if __name__ == '__main__':
    import json

    import requests

    URL = 'http://open-api.myhelsinki.fi/v1/events/'
    resp = requests.get(URL)
    with open('events-helsinki.json', 'w') as f:
        f.write(json.dumps(resp.json()))
