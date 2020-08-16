import requests
import json

# original request

API_KEY = '/&apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'
format_json = 'json'
# original sample for test api
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/test?apikey=l7xx2af7939c63424511946e0fcdc35fe22a

alma_haifa_host = "https://api-eu.hosted.exlibrisgroup.com"
alma_test_api = '/test?apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'
alma_path = "/almaws/v1/bibs"


def test_api_key():
    try:
        request_str = alma_haifa_host  + alma_path + alma_test_api
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type text ' +  str(type(response.text)) + ' type content ' + str(type(response.content)))
        try:
            # data = response.json() #Only convert to Json when status is OK.
            json_obj = response.text # json.loads(response.content)
        except Exception as e:
            print (e)

        print(response.text)



print('start test on api key')
collection_id = '81174994600002791'
test_api_key()