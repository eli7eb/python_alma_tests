import requests
import json

# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81174994600002791?level=1&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
# qwery is needed when I dont have the collection ID yet. If I have it I need to look if there are sub collections
# test to connect with alma
# get list of images from collection by collection name or ID
# get one image to display or to link (same thing actually)
API_KEY = '&apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'
API_KEY_FIRST = '?apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'

# collection ID for consul 8180019930000562

alma_host = "https://api-eu.hosted.exlibrisgroup.com"
alma_test_api = '/test?apikey=l8xx7153483e1e9e4d7099e8bf9a406f4642'
alma_path = "/almaws/v1"
alma_bibs = "/bibs"
alma_params_level = "?level="
alma_bibs_offset = '?offset='
alma_bibs_limit = '&limit='
alma_collections = "/collections/"
alma_format = '&format=json'
language_id = 'lang=iw_IL'
alma_representations = '/representations'
alma_files = '/files'
headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(API_KEY)}

haifa_url_call_end = '\''

def retrieve_collections():
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections?level=1&apikey=l7xx2af7939c63424511946e0fcdc35fe22a

    print ('retrieve_collections')
    collections = "/collections"
    call_params = '?level=1'
    request_str = alma_host + alma_path + alma_bibs + collections + call_params + API_KEY + alma_format
    try:
        print ('request {}'.format(request_str))
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type ' +  str(type(response)) + ' type content ' + str(type(response.content)))
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))
    print ('retrieve_collections end')


def retrieve_bibs_in_collection(collection_id,offset,limit):
    print ('retrieve_bibs_in_collection')
    # original is
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81165295290002791/bibs?offset=0&limit=10&apikey=l7xx2af7939c63424511946e0fcdc35fe22a

    try:
        call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
        request_str = alma_host + alma_path + alma_bibs + alma_collections + collection_id + alma_bibs + call_params + API_KEY + alma_format
        print ('request {}'.format(request_str))
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type ' +  str(type(response)) + ' type content ' + str(type(response.content)))
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))
    return data['bib']

# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/990013500690402791/representations?limit=10&offset=0&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
def retrieve_digital_representations(mms_data,offset,limit):
    alma_bibs_offset = '?offset='
    alma_bibs_limit = '&limit='

    mms_id =  mms_data[0]['mms_id']
    print ('retrieve_digital_representations')
    # original is
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/8180019930000562/representations?limit=100&offset=0&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
    try:
        call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
        request_str = alma_host + alma_path + alma_bibs + "/" + mms_id + alma_representations + call_params + API_KEY + alma_format
        print ('request {}'.format(request_str))
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        print('success code ' + str(response.status_code) + ' type ' +  str(type(response)) + ' type content ' + str(type(response.content)))
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))
        data_rep_list = data['representation'][0]
        rep_id = data_rep_list['id']
        return mms_id, rep_id # list of rep_id

# collection_id for api consul
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/8180019930000562?level=1&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
# mms_id for api consul
# book 99215535900562
# 991129830000541

def retrieve_collection(collection_id, level):
    print ('retrieve_collection')
    get_level = alma_params_level + str(level)
    alma_params = '&expand=d_avail'
    try:
        request_str = alma_host  + alma_path + alma_bibs + alma_collections + collection_id  + get_level + alma_params + API_KEY + alma_format
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))
        if 'mms_id' in data:
            mms_id_object = data['mms_id']
            print ('mms_id {}'.format(data["mms_id"]))
        if 'name' in data:
            mms_name = data['name']
            print ('mms_name {}'.format(mms_name))
        if 'description' in data:
            mms_description = data['description']
            print('mms_description {}'.format(mms_description))
    print('retrieve_collection end')
    return mms_id_object, mms_name, mms_description

# original request
#​/almaws​/v1​/bibs​/{mms_id}​/representations​/{rep_id}​/files Retrieve Representation Files' Details
def retrieve_representation_files_details(mms_id, rep_id):
    print ('retrieve_representation_files_details')
    try:
        request_str = alma_host  + alma_path + alma_bibs + '/' + mms_id + alma_representations + '/' + rep_id + alma_files + API_KEY_FIRST + alma_format
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))
        p_list = data['representation_file'][0]
        p_id = p_list['pid']
        return p_id  # list of rep_id

# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/99215535900562/representations/99215535900562?apikey=l7xx2af7939c63424511946e0fcdc35fe22a
def retrieve_representation_details(mms_id, rep_id):
    print ('retrieve_representation_details')
    try:
        request_str = alma_host  + alma_path + alma_bibs + '/' + mms_id + alma_representations + '/' + rep_id + API_KEY_FIRST + alma_format
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))

# /almaws/v1/bibs/{mms_id}/representations/{rep_id}/files/{file_id} Retrieve Representation File Details
def retrieve_representation_file_details(mms_id, rep_id, file_id):
    print ('retrieve_representation_file_details')
    try:
        request_str = alma_host  + alma_path + alma_bibs + '/' + mms_id + alma_representations + '/' + rep_id + alma_files + '/' + file_id + API_KEY_FIRST + alma_format
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as c_err:
        print(c_err)
    except requests.exceptions.HTTPError as err:  # This is the correct syntax
        print('error code ' + err)
    if response.status_code == 200:
        data = json.loads(response.content)
        print(json.dumps(data, indent=4, sort_keys=True))


print('retrieve collections')
retrieve_collections()
print('start test on collection ID')
collection_id = '81165295290002791'
collection_get_level = 2
mms_tuple = retrieve_collection(collection_id, collection_get_level)
# TODO make sure I have all more than 100 sometimes
mms_id_data = retrieve_bibs_in_collection(collection_id,0,10)
mms_id, rep_id = retrieve_digital_representations(mms_id_data, 0, 10)

#​/almaws​/v1​/bibs​/{mms_id}​/representations​/{rep_id} Retrieve Representation Details
retrieve_representation_details(mms_id, rep_id)
#​/almaws​/v1​/bibs​/{mms_id}​/representations​/{rep_id}​/files Retrieve Representation Files' Details
file_id = retrieve_representation_files_details(mms_id, rep_id)
# /almaws/v1/bibs/{mms_id}/representations/{rep_id}/files/{file_id} Retrieve Representation File Details
retrieve_representation_file_details(mms_id, rep_id, file_id)
