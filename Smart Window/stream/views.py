from builtins import print

from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import base64
import io
import cv2
from PIL import Image
import threading
import time

from .geography.geo_info import GeoLocationInfo
from .yolo import detector

global image_detector
image_detector = detector.YOLO()


def index(request):
    return render(request, 'stream/index.html')

def image_analysis(request):
    if request.method == "POST":
        print("this is post")
        data = json.loads(request.body)

        image = base64.b64decode(str(data.get("img")))
        img = Image.open(io.BytesIO(image))
        json_data = image_detector.detect_img(img)
        # image = 'opera.jpg'
        # img = Image.open(io.BytesIO(image))
        # r_image, ObjectsList = image_detector.detect_img(img)

    return JsonResponse(json_data)