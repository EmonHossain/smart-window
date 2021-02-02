import io
import cv2 as cv2
import requests
import base64
import numpy as np
import json
from flask import Flask, request, render_template
from flask import Response
from PIL import Image # pip  install pillow
from imageai.Detection import ObjectDetection
import os

app = Flask(__name__)
""" global varible variable """
image_np = np.array([1, 2, 3, 4, 5])


@app.route('/')
def webcam():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/URL_tesing')
def URL_tesing():
    """Video streaming home page."""
    global image_np
    print(image_np)
    print(type(image_np))
    return render_template('image_data.html')

@app.route('/get_image_data', methods=['POST'])
def get_image_data():
    """Getting the image data in json form, from the ajax request"""
    jsonResponse =  request.get_json()
    json_data= {
        'image': jsonResponse
    }
    image = jsonResponse['image']
    base64_decoded = base64.b64decode(image.split(',')[1])
    f = open("image.jpg", "wb")
    f.write(base64_decoded)
    f.close()
    #global arr
    #arr = cv2.bitwise_not(cv2.imread("temp.png", 0))
    #image = Image.open(io.BytesIO(base64_decoded))
    #global image_np
    #image_np = np.array(image)
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "image.jpg"),
                                                 output_image_path=os.path.join(execution_path, "imagenew.jpg"))

    for eachObject in detections:
        print(eachObject["name"], " : ", eachObject["percentage_probability"])
    return Response(json.dumps(json_data))



@app.route('/get_geolocation_data', methods=['POST'])
def get_geolocation_data():
    """Getting the data from the ajax request and api"""
    geolocation = request.get_json()
    loc = (str(geolocation['loc'])).split(", ")
    lat = float(loc[0])
    long = float(loc[1])
    # api-endpoint
    URL = "https://places.ls.hereapi.com/places/v1/discover/explore"
    # API key
    api_key = 'tCLOWQv2DtK02jWzK7lxRq933DNH8HrE7chf60cE_-c'
    # Defining a params dictionary for the parameters to be sent to the API
    PARAMS = {
        'at': '{},{}'.format(lat, long),
        'apikey': api_key,
        'cat': "Landmark-Attraction",
    }

    # Sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # Extracting data in json format
    data = r.json()
    # Taking out title from JSON
    museum = []
    landmark = []
    landmark_distance = []
    museum_distance = []
    count1 = 0
    count2 = 0
    for info in data['results']['items']:
        if (info['category']['id'] == "museum" and count1 < 3):
            museum.append(info['title'])
            museum_distance.append((info['distance']))
            count1 = count1 + 1
        if (info['category']['id'] == "landmark-attraction" and count2 < 3):
            landmark.append(info['title'])
            landmark_distance.append((info['distance']))
            count2 = count2 + 1
    museums = museum
    landmarks_distance = landmark_distance
    landmarks = landmark
    museums_distance = museum_distance
    current_location = data['search']['context']['location']['address']['text']
    current_loc = current_location.split("<br/>")
    json_data = {
        'museums': museum,
        'landmarks_distance': landmark_distance,
        'landmarks': landmark,
        'museums_distance': museum_distance,
        'current_loc': current_loc,
        'lat': lat,
        'long': long,
    }
    return Response(json.dumps(json_data))



if __name__ == '__main__':
    app.run(debug=True)
