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



