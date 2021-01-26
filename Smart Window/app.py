import cv2 as cv2
import requests
import json
from flask import Flask, request, render_template
from flask import Response


app = Flask(__name__)
camera = cv2.VideoCapture(0)  # use 0 for web camera



# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    global geolocation, address
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:

            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            # video frame
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def webcam():
    """Video streaming home page."""
    global landmarks, museums, museums_distance, landmarks_distance, current_loc
    return render_template('index.html')

@app.route('/getdata', methods=['POST'])
def getdata():
    """Getting the data form the ajax request and api"""
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
