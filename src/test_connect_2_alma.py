import requests
import json
from json2html import *

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
# one function to handle all ALMA calls and error codes
def alma_url_call(request_str,to_print):
    print('alma_url_call')
    try:
        print('request {}'.format(request_str))
        response = requests.request("GET", request_str)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTPError ".format(err))
    except requests.exceptions.Timeout as err:
        print("Timeout ".format(err))
    except requests.exceptions.ConnectionError as err:
        print("ConnectionError ".format(err))
    except requests.exceptions.TooManyRedirects as err:
        print("TooManyRedirects ".format(err))
    except requests.exceptions.RequestException as err:
        print("RequestException ".format(err))
        raise SystemExit(err)
    print('success code ' + str(response.status_code) + ' type ' + str(type(response)) + ' type content ' + str(
        type(response.content)))
    data = json.loads(response.text)
    if to_print:
        print(json.dumps(data, indent=4, sort_keys=True))

    print('alma_url_call end ')
    return data
# test api key
# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/test?apikey=l7xx2af7939c63424511946e0fcdc35fe22a
#
def test_api_key():
    print ('test_api_key')
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/test?apikey=l7xx2af7939c63424511946e0fcdc35fe22a
    request_str = alma_host + alma_path + alma_bibs + alma_test_api + alma_format
    alma_url_call(request_str,True)
    print('test_api_key end')

def retrieve_collections():
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections?level=1&apikey=l7xx2af7939c63424511946e0fcdc35fe22a

    print ('retrieve_collections')
    collections = "/collections"
    call_params = '?level=2'
    request_str = alma_host + alma_path + alma_bibs + collections + call_params + API_KEY + alma_format
    data = alma_url_call(request_str,True)
    collections = data['collection']
    create_html_4_collection_list('collections list',collections,'collections_list_file.html')
    create_html_list_of_collection_level_2('collections list level 2',collections,'collections_list_level_2_file.html')
    for c in collections:
        print ('collection id {} name {}'.format(str(c['pid']['value']), c['name']))
    print ('retrieve_collections end')
    return collections

# original request /almaws/v1/bibs/{mms_id}
def retrieve_bibs_by_mms_id(collections_list):
    print('retrieve_bibs_by_mms_id')
    for c in collections_list:
        print ('collection')
        mms_id = str(c['mms_id']['value'])
        request_str = alma_host + alma_path + alma_bibs + '/' + mms_id + API_KEY_FIRST + alma_format
        data = alma_url_call(request_str,True)

    print('retrieve_bibs_by_mms_id end')


# the first call is a must to set the total number of items in collection
# it can be done more inteligently if I had more time
def retrieve_total_number_of_bibs_in_collection(collection_id,offset,limit):
    print ('retrieve_bibs_in_collection')
    # original is
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81165295290002791/bibs?offset=0&limit=10&apikey=l7xx2af7939c63424511946e0fcdc35fe22a

    call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
    request_str = alma_host + alma_path + alma_bibs + alma_collections + collection_id + alma_bibs + call_params + API_KEY + alma_format
    data = alma_url_call(request_str,False)
    bibs = data['bib']
    total_records_count = data['total_record_count']
    for b in bibs:
        print('bib id {} name {}'.format(str(b['mms_id']), b['title']))
    print(json.dumps(data, indent=4, sort_keys=True))

    return total_records_count

# get all mms data calling 100 and then another 100 until total
# by iteraing the 100 until no more is found
def retrieve_list_of_bibs_in_collection(collection_id, total_items):
    print ('retrieve_bibs_in_collection')
    # original is
    # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/81165295290002791/bibs?offset=0&limit=10&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
    offset = 0
    limit = 100
    mms_list = []
    while offset < total_items:
        call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
        request_str = alma_host + alma_path + alma_bibs + alma_collections + collection_id + alma_bibs + call_params + API_KEY + alma_format
        data = alma_url_call(request_str,False)
        if 'bib' in data:
            bibs = data['bib']
            # I want one list so loop over the inner list and append
            for b in bibs:
                mms_list.append(b)
            offset += limit
        else:
            print ('check out')
    return mms_list

def create_html_4_mms_id(mms_dict,title,file_name):

    print('create_html_4_mms_id')
    fileout = open(file_name, "w")
    table = "<html>"
    table += "\n<head>"
    table += '\n<title>' + title + '</title>\n'
    style = "<style>"
    style += "p { margin: 0 !important;  }"
    style += "table ,td,th {table-layout: fixed; border-collapse: separate ;border: 1px solid black;} "
    style += "</style>"
    table += style
    # "</head>\n<style>p { margin: 0 !important;  } table {table-layout: fixed; border-collapse: collapse;border: 1px solid black;} </style>"

    table += "\n<body>\n"
    table += '\n<p>'
    table += '\n<h1>' + title + '</h1>\n'
    table += '</p>\n'
    table += '\n<p>'
    table += "<table>\n"
    table += "  <tr>\n"
    header = ['index', 'id', 'description', 'delivery_url','image link', 'image', 'thumbnail link', 'thumbnail image']
    table += "  <tr>\n"
    for line in header:
        table += "    <td>{0}</td>\n".format(line)
    table += "  </tr>\n"
    counter = 1
    for line_data in mms_dict.items():
        line = line_data[1]
        table += "  <tr>\n"
        table += "    <td>{0}</td>\n".format(str(counter))
        table += "    <td>{0}</td>\n".format(str(line['id']))
        table += "    <td>{0}</td>\n".format(str(line['title']))
        delivery_link = '<a href = {0!s}>delivery</a>'.format(line['delivery_url'])
        table += "    <td>{0!s}</td>\n".format(delivery_link)
        image_link = '<a href = {0!s}>image link</a>'.format(line['image_url'])
        table += "    <td>{0!s}</td>\n".format(image_link)
        size_image = '<img src = "{0!s}" alt = "image">'.format(line['image_url'])
        table += "    <td>{0!s}</td>\n".format(size_image)
        thumb_link = '<a href = {0!s}>thumbnail</a>'.format(line['thumbnail_url'])
        table += "    <td>{0!s}</td>\n".format(thumb_link)
        thumb_image = '<img src = "{0!s}" alt = "image">'.format(line['thumbnail_url'])
        table += "    <td>{0!s}</td>\n".format(thumb_image)
        table += "  </tr>\n"
        counter += 1
    table += "</table>"
    table += '</p>\n'
    table += '</body>\n'
    table += "</html>"
    fileout.writelines(table)
    fileout.close()

# list of collections and children
def create_html_list_of_collection_level_2(title,data,file_name):
    print ('create_html_list_of_collection_level_2')
    fileout = open(file_name, "w")
    table = "<html>"
    table += "\n<head>"
    table += '\n<title>' + title + '</title>\n'
    style = "<style>"
    style += "p { margin: 0 !important;  }"
    style += "table ,td,th {table-layout: fixed; border-collapse: separate ;border: 1px solid black;} "
    style += "</style>"
    table += style
    # "</head>\n<style>p { margin: 0 !important;  } table {table-layout: fixed; border-collapse: collapse;border: 1px solid black;} </style>"

    table += "\n<body>\n"
    table += '\n<p>'
    table += '\n<h1>' + title + '</h1>\n'
    table += '</p>\n'

    # add for loop for each table, there are few for loops but one table per loop
    for d in data:
        table_title = "PID: {} Mms_Id: {} Name: {}".format(str(d['pid']['value']), str(d['mms_id']['value']), str(d['name']))
        table += '\n<p>'
        table += '\n<h2>' + table_title + '</h2>\n'
        table += '</p>\n'
        table += '\n<p>'
        table += "<table>\n"
        table += "  <tr>\n"
        header = ['counter', 'pid', 'mms_id', 'name', 'description']
        table += "  <tr>\n"
        for line in header:
            table += "    <td>{0}</td>\n".format(line)
        table += "  </tr>\n"
        counter = 1
        if 'collection' in d.keys():
            for c in d['collection']:
                table += "  <tr>\n"
                table += "    <td>{0}</td>\n".format(str(counter))
                table += "    <td>{0}</td>\n".format(str(c['pid']['value']))
                table += "    <td>{0}</td>\n".format(str(c['mms_id']['value']))
                table += "    <td>{0}</td>\n".format(str(c['name']))
                table += "    <td>{0}</td>\n".format(str(c['description']))
                counter += 1
                table += "  </tr>\n"
            table += "</table>"
            table += '</p>\n'
            table += '</body>\n'
            table += "</html>"
        else:
            print ('no level data')
            table += "</table>"
            table += '</p>\n'
            table += '</body>\n'
            table += "</html>"

    fileout.writelines(table)
    fileout.close()
    print('create_html_list_of_collection_level_2 end')


def create_html_4_collection_list(title,data,file_name):
    print('create_html_4_collection_list')
    fileout = open(file_name, "w")
    table = "<html>"
    table += "\n<head>"
    table += '\n<title>' + title + '</title>\n'
    style = "<style>"
    style += "p { margin: 0 !important;  }"
    style +=  "table ,td,th {table-layout: fixed; border-collapse: separate ;border: 1px solid black;} "
    style += "</style>"
    table += style
        # "</head>\n<style>p { margin: 0 !important;  } table {table-layout: fixed; border-collapse: collapse;border: 1px solid black;} </style>"


    table += "\n<body>\n"
    table += '\n<p>'
    table += '\n<h1>' + title + '</h1>\n'
    table += '</p>\n'
    table += '\n<p>'
    table += "<table>\n"
    table += "  <tr>\n"
    header = ['counter', 'id','mms_id','name','description']
    table += "  <tr>\n"
    for line in header:
        table += "    <td>{0}</td>\n".format(line)
    table += "  </tr>\n"
    counter = 1
    for line in data:
        table += "  <tr>\n"
        table += "    <td>{0}</td>\n".format(str(counter))
        table += "    <td>{0}</td>\n".format(str(line['pid']['value']))
        table += "    <td>{0}</td>\n".format(str(line['mms_id']['value']))
        table += "    <td>{0}</td>\n".format(str(line['name']))
        table += "    <td>{0}</td>\n".format(str(line['description']))
        counter += 1
        table += "  </tr>\n"

    table += "</table>"
    table += '</p>\n'
    table += '</body>\n'
    table += "</html>"
    fileout.writelines(table)
    fileout.close()

def create_html_for_collections_level_2(line):
    print ('create_html_for_collections_level_2')
    print('create_html_for_collections_level_2 end')


def create_html_4_collection(title,data,file_name):
    print('create_html_4_collection')
    fileout = open(file_name, "w")
    table = "<html>"
    table += "\n<head>"
    table += '\n<title>' + title + '</title>\n'
    style = "<style>"
    style += "p { margin: 0 !important;  }"
    style +=  "table ,td,th {table-layout: fixed; border-collapse: separate ;border: 1px solid black;} "
    style += "</style>"
    table += style
        # "</head>\n<style>p { margin: 0 !important;  } table {table-layout: fixed; border-collapse: collapse;border: 1px solid black;} </style>"


    table += "\n<body>\n"
    table += '\n<p>'
    table += '\n<h1>' + title + '</h1>\n'
    table += '</p>\n'
    table += '\n<p>'
    table += "<table>\n"
    table += "  <tr>\n"
    header = ['id','name','description']
    table += "  <tr>\n"
    for line in header:
        table += "    <td>{0}</td>\n".format(line)
    table += "  </tr>\n"

    for line in data:
        table += "  <tr>\n"
        table += "    <td>{0}</td>\n".format(str(line['pid']['value']))
        table += "    <td>{0}</td>\n".format(str(line['name']))
        table += "    <td>{0}</td>\n".format(str(line['description']))
        table += "  </tr>\n"
    table += "</table>"
    table += '</p>\n'
    table += '</body>\n'
    table += "</html>"
    fileout.writelines(table)
    fileout.close()


# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/990013500690402791/representations?limit=10&offset=0&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
# returns a dictionary of mms_id and title link amd rep_id
def retrieve_digital_representations(colletion_id, mms_list_data):
    offset = 0
    limit = 100
    count = 0
    alma_bibs_offset = '?offset='
    alma_bibs_limit = '&limit='
    mms_dict = {}
    for l in mms_list_data:
        mms_id = l['mms_id']
        print ('retrieve_digital_representations count {} total {}'.format(str(count),str(len(mms_list_data))))
        # original is
        # https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/8180019930000562/representations?limit=100&offset=0&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
        call_params = alma_bibs_offset + str(offset) + alma_bibs_limit + str(limit)
        request_str = alma_host + alma_path + alma_bibs + "/" + mms_id + alma_representations + call_params + API_KEY + alma_format
        data = alma_url_call(request_str,False)
        data_rep_list = data['representation'][0]
        title_item = {'title':l['title']}
        data_rep_list.update(title_item)
        # add the correct link to the real size image
        correct_size_image_url = str(data_rep_list['thumbnail_url']).replace('thumbnail/','')
        image_url = {'image_url':correct_size_image_url}
        data_rep_list.update(image_url)

        mms_dict[mms_id] = data_rep_list
        count += 1
        if count == 50:
            break

    mms_file_name = 'mms_list_collection_id_{0!s}.html'.format(colletion_id)
    title = 'mms list 4 collection {0!s}'.format(colletion_id)
    create_html_4_mms_id(mms_dict,title,mms_file_name)
    return mms_dict # dict of representations of mms_id's

# collection_id for api consul
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/8180019930000562?level=1&apikey=l7xx2af7939c63424511946e0fcdc35fe22a
# mms_id for api consul
# book 99215535900562
# 991129830000541

def retrieve_collection_information(collection_id, level):
    print ('retrieve_collection')
    get_level = alma_params_level + str(level)
    alma_params = '&expand=d_avail'
    request_str = alma_host  + alma_path + alma_bibs + alma_collections + collection_id  + get_level + alma_params + API_KEY + alma_format
    data = alma_url_call(request_str,False)
    if 'parent_pid' in data:
        parent_pid_object = data['parent_pid'] if data['parent_pid'] else None
        print ('mms_id {}'.format(data["parent_pid"]))
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
    collection_info_dict = dict(collection_parent=parent_pid_object, collection_mms_id=mms_id_object, collection_name=mms_name, collection_desc=mms_description)
    return collection_info_dict

# original request
#​/almaws​/v1​/bibs​/{mms_id}​/representations​/{rep_id}​/files Retrieve Representation Files' Details
def retrieve_representation_files_details(mms_dict):
    print ('retrieve_representation_files_details')
    images_file_data = {}
    for mms_id, rep_item in mms_dict.items():
        rep_id = rep_item[0]['id']
        request_str = alma_host  + alma_path + alma_bibs + '/' + mms_id + alma_representations + '/' + rep_id + alma_files + API_KEY_FIRST + alma_format
        data = alma_url_call(request_str,False)
        p_list = data['representation_file'][0]
        images_file_data[mms_id] = rep_item,p_list
    return images_file_data  # list of rep_id

# original request
# https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/99215535900562/representations/99215535900562?apikey=l7xx2af7939c63424511946e0fcdc35fe22a
def retrieve_representation_details(mms_dict):
    print ('retrieve_representation_details')
    for mms_id, rep_item in mms_dict.items():
        rep_id = rep_item[0]['id']
        request_str = alma_host  + alma_path + alma_bibs + '/' + mms_id + alma_representations + '/' + rep_id + API_KEY_FIRST + alma_format
        data = alma_url_call(request_str,False)
        print(json.dumps(data, indent=4, sort_keys=True))

# /almaws/v1/bibs/{mms_id}/representations/{rep_id}/files/{file_id} Retrieve Representation File Details
def retrieve_representation_file_details(image_dict):
    print ('retrieve_representation_file_details')
    for mms_id, image_item in image_dict.items():
        rep_object= image_item[0]
        file_object = image_item[1]
        # rep_item is a tuple
        rep_id = rep_object[0]['id']
        file_id = file_object['pid']
        request_str = alma_host  + alma_path + alma_bibs + '/' + mms_id + alma_representations + '/' + rep_id + alma_files + '/' + file_id + API_KEY_FIRST + alma_format
        data = alma_url_call(request_str,False)
        print(json.dumps(data, indent=4, sort_keys=True))

# test_api_key()
print('retrieve collections')
collections_list = retrieve_collections()
print('start test on collection ID')
retrieve_bibs_by_mms_id(collections_list)
# קהאן הצלם 81164644630002791
# קבוצת כנרת 81165295290002791
collection_id = '81165295290002791'
collection_get_level = 2
# returns a dict w parent mms_id collection_name collection_desc
collection_dict = retrieve_collection_information(collection_id, collection_get_level)
number_of_items = 100
# # TODO make sure I have all more than 100 sometimes
total_items = retrieve_total_number_of_bibs_in_collection(collection_id,0,number_of_items)
mms_list = retrieve_list_of_bibs_in_collection(collection_id,total_items)
print ('digital representations part')
# # digital representations part
# /almaws/v1/bibs/{mms_id}/representations
# This web service returns a list of Digital Representations for a given Bib MMS-ID.
mms_dict = retrieve_digital_representations(collection_id, mms_list)
# #​/almaws​/v1​/bibs​/{mms_id}​/representations​/{rep_id} Retrieve Representation Details
# retrieve_representation_details(mms_dict)
# #​/almaws​/v1​/bibs​/{mms_id}​/representations​/{rep_id}​/files Retrieve Representation Files' Details
# image_dict = retrieve_representation_files_details(mms_dict)
# # /almaws/v1/bibs/{mms_id}/representations/{rep_id}/files/{file_id} Retrieve Representation File Details
# retrieve_representation_file_details(image_dict)
