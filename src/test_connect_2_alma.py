import requests
import json
import xml.etree.ElementTree as ElementTree


# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81174994600002791?level=1&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
# qwery is needed when I dont have the collection ID yet. If I have it I need to look if there are sub collections
# test to connect with alma
# get list of images from collection by collection name or ID
# get one image to display or to link (same thing actually)
API_KEY = '&apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'
format_json = 'json'



alma_host = "https://api-eu.hosted.exlibrisgroup.com"
alma_test_api = '/test?apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'
alma_path = "/almaws/v1"
alma_bibs = "/bibs"
alma_params_level = "?level="
alma_bibs_offset = '?offset='
alma_bibs_limit = '&limit='
alma_collections = "/collections/"

language_id = 'lang=iw_IL'
headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(API_KEY)}
query_params = { "format": format_json }
haifa_url_call_end = '\''

def retrieve_bibs_4_collection(collection_id,offset,limit):
    print ('retrieve_bibs_4_collection')
    # original is
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81165295290002791/bibs?offset=0&limit=10&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
    mms_id_list = []
    try:
        call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
        request_str = alma_host + alma_path + alma_bibs + alma_collections + collection_id + alma_bibs + call_params + API_KEY
        print ('request {}'.format(request_str))
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type ' +  str(type(response)) + ' type content ' + str(type(response.content)))
        try:
            root = ElementTree.fromstring(response.content)
            counter = 0
            for child in root.iter('*'):
                print ('counter  {} child {}'.format(str(counter),child))
                if (child.tag == 'mms_id'):
                    print ('mms_id ' + child.text)
                    mms_id_list.append(child.text)
                print("counter {} tag {} atttib {}".format(str(counter), child.tag,  child.attrib))
                counter+=1
            print ('total '+counter)
            # print(response.json()) # json.loads(response.content.decode('utf-8')) #  response.json()
            # json_obj = response.text # json.loads(response.content)
        except Exception as e:
            print (e)
    return mms_id_list

def retrieve_digital_representation_4_collection(collection_id,offset,limit):
    print ('retrieve_bibs_4_collection')
    # original is
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81165295290002791/bibs?offset=0&limit=10&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
    try:
        call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
        request_str = alma_host + alma_path + alma_bibs + alma_collections + collection_id + alma_bibs + call_params + API_KEY
        print ('request {}'.format(request_str))
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type ' +  str(type(response)) + ' type content ' + str(type(response.content)))
        try:
            root = ElementTree.fromstring(response.content)
            counter = 0
            for child in root.iter('*'):
                print("counter {} tag {} atttib {}".format(str(counter), child.tag,  child.attrib))
                counter+=1
            print ('total '+counter)
            # print(response.json()) # json.loads(response.content.decode('utf-8')) #  response.json()
            # json_obj = response.text # json.loads(response.content)
        except Exception as e:
            print (e)


def test_search_by_collection_id(collection_id, level):
    get_level = alma_params_level + str(level)
    try:
        request_str = alma_host  + alma_path + alma_collections + collection_id  + get_level + API_KEY # prefix_haifa + prefix_collection + collections+ collection_id + API_KEY
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type ' +  str(type(response)) + ' type content ' + str(type(response.content)))
        try:
            root = ElementTree.fromstring(response.content)
            counter = 0
            for child in root.iter('*'):
                print("counter {} tag {} atttib {}".format(str(counter), child.tag,  child.attrib))
                counter+=1
            print ('total '+counter)
            # print(response.json()) # json.loads(response.content.decode('utf-8')) #  response.json()
            # json_obj = response.text # json.loads(response.content)
        except Exception as e:
            print (e)

        print(response.text)
        print ('json')
        #print('json objects {}'.format(json_obj['artObjects']))

def parse_mms_id_list(mms_id_list):
    print ('parse_mms_id_list')
    for l in mms_id_list:
        print ('go for mms_id {}'.format(l))
        mms_id_str = '/'+l+'/representations'

        try:
            request_str = alma_host + alma_path + alma_bibs + mms_id_str + API_KEY
            response = requests.request("GET", request_str)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as c_err:
            print(c_err)
        except requests.exceptions.HTTPError as err:  # This is the correct syntax
            print('error code ' + err)
        if response.status_code == 200:
            print('success code ' + str(response.status_code) + ' type ' + str(type(response)) + ' type content ' + str(
                type(response.content)))

print('start test on collection ID')
collection_id = '81165295290002791'
collection_get_level = 2
#test_search_by_collection_id(collection_id, collection_get_level)
mms_id_data = retrieve_bibs_4_collection(collection_id,0,10)
print (mms_id_data)
parse_mms_id_list(mms_id_data)