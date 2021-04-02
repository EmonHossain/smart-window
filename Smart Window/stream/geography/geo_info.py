import requests


class GeoLocationInfo:

    def get_api_data(self, lat, long):

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
        response = requests.get(url=URL, params=PARAMS)

        # Extracting data in json format
        data = response.json()
        # Taking out title from JSON
        museums = []
        landmarks = []

        for info in data['results']['items']:
            if info['category']['id'] == "museum":
                museum = {
                    "title": info['title'],
                    "distance": info['distance'],
                    "img": "",
                }
                if info['title'] == "Museum Roter Turm":
                    museum["img"] = "/static/stream/images/Roter_Turm.jpg"
                museums.append(museum)

            if info['category']['id'] == "landmark-attraction":
                landmark = {
                    "title": info['title'],
                    "distance": info['distance'],
                    "img": "",
                }
                if info['title'] == "Karl-Marx-Monument":
                    landmark["img"] = "/static/stream/images/cm.png"

                landmarks.append(landmark)

        current_location = data['search']['context']['location']['address']['text']
        print(current_location)
        current_loc = current_location.split("<br/>")
        json_data = {
            'museums': museums,
            'landmarks': landmarks,
            'current_loc': current_loc,
        }
        # json_data['f'] ='test'
        print(json_data)
        return json_data
