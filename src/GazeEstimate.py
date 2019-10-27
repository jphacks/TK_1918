#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Gaze Estimation API Client ################################################

import os
import sys
import time
import math
import json
import base64
import requests
import cv2
import numpy

## Settings ###################################################################

endPoint = 'http://a8b88762ef01211e9950f0eacce6e863-2021028779.ap-northeast-1.elb.amazonaws.com'       # for JPHACKS 2019

proxies = []
#proxies = ['http':'http://proxygate2.nic.nec.co.jp:8080', 'https':'http://proxygate2.nic.nec.co.jp:8080']

displayFlag = False

###############################################################################

# Send Request
def sendRequest(frame):
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width  = imgGray.shape
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
    res = requests.post(url, params=params, data=data, headers=headers, proxies=proxies, timeout=10)

    # Get response
    if res.status_code == 200:
        return res.json()
    else:
        print('## Error! ##')
        print(res.text)
        return []

def estimateGaze(img):
    results = sendRequest(img)

    # Show result
    print(json.dumps(results, indent=4))
    return(results)
    if displayFlag:
        width = img.shape[1]
        gazeLen = width / 5
        gazeColor = (0,255,0)
        eyesColor = (255,0,0)


    for result in results:
            reye = result['reye']
            leye = result['leye']
            gaze = result['gaze']

            # Show the result
            #cv2.circle(img, (int(reye[0]), int(reye[1])), 15, eyesColor, thickness=2)
            #cv2.circle(img, (int(leye[0]), int(leye[1])), 15, eyesColor, thickness=2)
            center = ((reye[0]+leye[0])/2, (reye[1]+leye[1])/2)
            gazeTop = (center[0] + gazeLen * math.sin(math.radians(gaze[0])), center[1] + gazeLen * math.sin(math.radians(gaze[1])))
            #cv2.arrowedLine(img, (int(center[0]), int(center[1])), (int(gazeTop[0]), int(gazeTop[1])), gazeColor, thickness=2)

            #cv2.imwrite("gaze_output.png",img)
            #cv2.imshow('image', img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()


