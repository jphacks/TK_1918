#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Gaze Estimation API Client ################################################
__author__  = "Yoshi Kajiki <y-kajiki@ah.jp.nec.com>"
__version__ = "0.9"
__date__    = "Oct 18, 2019"

import os
import sys
import time
import math
import cv2
import json
import base64
import requests
import numpy
import threading
import queue

## Settings ###################################################################

frameRateAPI = 1
delayTime = 1.0

endPoint = 'http://a8b88762ef01211e9950f0eacce6e863-2021028779.ap-northeast-1.elb.amazonaws.com'       # for JPHACKS 2019

proxies = []
#proxies = ['http':'http://proxygate2.nic.nec.co.jp:8080', 'https':'http://proxygate2.nic.nec.co.jp:8080']

maxNumThread = 10

###############################################################################
def estimateGazeTh(frameNo, image, width, height, resultQueue):
    global endPoint
    global proxies

    # Extrace RAW image
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgRawArray = numpy.reshape(imgGray, (-1))
    imgRaw = imgRawArray.tobytes()

    # Set URL
    url = endPoint + "/v1/query/gaze_byRAW"

    # Set request parameter
    reqPara = {
        'width' : width,
        'height' : height,
        'raw_b64' : base64.b64encode(imgRaw).decode('utf-8')
    }

    # Send the request
    headers = {'Content-Type' : 'application/json'}
    params = {}
    data = json.dumps(reqPara).encode('utf-8')
    res = requests.post(url, params=params, data=data, headers=headers, proxies=proxies, timeout=3)

    # Get response
    if res.status_code == 200:
        # print(json.dumps(res.json(), indent=4))
        result = {
            'frameNo' : frameNo,
            'gazeResult' : res.json()
        }
    else:
        print('## Error! ##')
        print(res.text)
        result = {
            'frameNo' : frameNo
        }
    resultQueue.put(result)

###############################################################################
def resultMargerTh(inVideoBuffer, resultQueue, outVideoBuffer):

    while True:
        frame = inVideoBuffer.get(block=True)
        frameNo = frame['frameNo']
        if frame['gazeEstimate']:
            while True:
                result = resultQueue.get(block=True)
                if result['frameNo'] == frameNo:
                    if 'gazeResult' in result:
                        frame['gazeResult'] = result['gazeResult']
                    outVideoBuffer.put(frame)
                    break
                else:
                    if time.time() > frame['showTime']:
                        frame['gazeEstimate'] = False
                        outVideoBuffer.put(frame)
                        break
                    resultQueue.put(result)
                    time.sleep(0.001)
        else:
            outVideoBuffer.put(frame)

###############################################################################
def videoReaderTh(videoSource, inVideoBuffer, resultQueue):
    global delayTime
    global frameRateAPI

    frameIntervalAPI = 1. / frameRateAPI
    privTimeAPI = 0

    # Open the Video
    try:
        video = cv2.VideoCapture(videoSource)
    except:
        print('Error!  Can not open the video [%s].' % videoSource)
        return
    if not video.isOpened():
        print('Error!  Can not open the video [%s].' % videoSource)
        return

    # Read Parameters of the Video
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video.get(cv2.CAP_PROP_FPS)
    interval = 1. / fps
    results = []
    gaze = None
    gazeLen = width / 5

    # Read the Video Stream
    while True:

        # Read a frame
        success, image = video.read()
        stTime = time.time()
        while not success:
            video.release()
            time.sleep(0.5)     # Just a moment
            print('### restart')
            video = cv2.VideoCapture(videoSource)
            success, image = video.read()
            stTime = time.time()
            results = []
        frameNo = video.get(cv2.CAP_PROP_POS_FRAMES)
        frame = {
            'showTime' : time.time() + delayTime,
            'frameNo' : frameNo,
            'image' : image,
            'gazeEstimate' : False
        }

        # call the gaze estimation API with frameRateAPI
        if time.time() - privTimeAPI > frameIntervalAPI:

            # exec thread
            threadNum = threading.active_count()
            #print('    thread num = %d' % threadNum)
            if threadNum < maxNumThread:
                th = threading.Thread(target=estimateGazeTh, args=([frameNo, image, width, height, resultQueue]), daemon=True)
                th.start()
                frame['gazeEstimate'] = True
            else:
                print('## Drop the frame No.%d' % int(frameNo))
                pass

            privTimeAPI = time.time()

        # Put the frame to videoBuffer
        inVideoBuffer.put(frame)

        # Wait for the next frame
        while time.time() - stTime < interval:
            time.sleep(0.001)

### Main ######################################################################
if __name__ == "__main__":

    argvs = sys.argv
    argc = len(argvs)
    #if argc < 2:
    #    print('Usage: python3 %s videoSource' % argvs[0])
    #    sys.exit(1)
    #videoSource = argvs[1]
    videoSource=0

    # initialize
    inVideoBuffer = queue.Queue()
    resultQueue = queue.Queue()
    outVideoBuffer = queue.Queue()
    gazeResult = []
    gazeColor = (0,255,0)
    eyesColor = (255,0,0)

    # start video reader thread
    th1 = threading.Thread(target=videoReaderTh, args=([videoSource, inVideoBuffer, resultQueue]), daemon=True)
    th1.start()

    # start result marger thread
    th2 = threading.Thread(target=resultMargerTh, args=([inVideoBuffer, resultQueue, outVideoBuffer]), daemon=True)
    th2.start()

    # Read the Video Buffer
    while True:
        frame = outVideoBuffer.get(block=True)
        showTime = frame['showTime']
        image = frame['image']
        while time.time() < showTime:
            time.sleep(0.001)

        # update results
        if 'gazeResult' in frame:
            gazeResult = frame['gazeResult']

        #######################################################################
        # Edit for your application
        #######################################################################
        width = image.shape[1]
        gazeLen = width / 5
        for face in gazeResult:
            reye = face['reye']
            leye = face['leye']
            gaze = face['gaze']

            cv2.circle(image, (int(reye[0]), int(reye[1])), 15, eyesColor, thickness=2)
            cv2.circle(image, (int(leye[0]), int(leye[1])), 15, eyesColor, thickness=2)
            center = ((reye[0]+leye[0])/2, (reye[1]+leye[1])/2)
            gazeTop = (center[0] + gazeLen * math.sin(math.radians(gaze[0])), center[1] + gazeLen * math.sin(math.radians(gaze[1])))
            cv2.arrowedLine(image, (int(center[0]), int(center[1])), (int(gazeTop[0]), int(gazeTop[1])), gazeColor, thickness=2)

        # show the video with gaze
        cv2.imshow('video', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            sys.exit(0)

