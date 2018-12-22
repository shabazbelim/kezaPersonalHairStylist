import os
from flask import Flask, jsonify, request

from hairstylist import BASE_DIR,STATIC_IMAGE_PATH, app
import pandas as pd
import json, base64
from hairstylist.api.constant import *
from hairstylist.pipeline.KEZA import return_image

field_data = None


@app.route('/')
def lol():
    return "lol"


@app.route('/uploaddesk', methods=['POST'])
def uploadform():
    data = response_format()
    try:
        request_json = request.get_json(silent=True, force=True)
        if request_json.get('id') is None and request_json.get('image'):
            raise Exception("misisng")
        # print(request_json)
        with open(STATIC_IMAGE_PATH +request_json['id']+request_json['ext'], "wb") as vid:
            image = base64.b64decode(request_json['image'].partition(",")[2])
            vid.write(image)
        links = return_image(STATIC_IMAGE_PATH + request_json['id'] + request_json['ext'])

        sugg = []
        for i in links:
            d = dict()
            d['link'] = 'img/' + i
            d['like'] = False
            d['id'] = i
            sugg.append(d)

        data['id'] = request_json.get('id')
        data['suggestions'] = sugg

    except Exception as e:
        print(e)
        data['id'] = "NA"
        data['suggestions'] = []
        # print(request_json)
    response = dict()
    response["status_code"] = 200
    response["data"] = data
    return jsonify(response)


@app.route('/upload', methods=['POST'])
def upload():
    data = response_format()
    response = dict()
    try:
        request_json = request.get_json(silent=True, force=True)

        if request_json.get('id') is None and request_json.get('image'):
            raise Exception("missing")
        # print(request_json)
        with open(STATIC_IMAGE_PATH + request_json['id']+request_json['ext'], "wb") as vid:
            image = base64.b64decode(request_json['image'])
            vid.write(image)
        links = return_image(STATIC_IMAGE_PATH + request_json['id']+request_json['ext'])

        if not links:
            response["status_code"] = 300
            response['message'] = "Face not captured properly."
            data = dict()
        else:
            sugg = []
            for i in links:
                d = dict()
                d['link'] = 'img/'+i
                d['like'] = False
                d['id'] = i
                sugg.append(d)

            data['id'] = request_json.get('id')
            response["status_code"] = 200
            response['message'] = "Success"
            data['suggestions'] = sugg

    except Exception as e:
        print(e)
        data['id'] = "NA"
        response["status_code"] = 500
        data['suggestions'] = []
    # print(request_json)


    response["data"] = data
    print(response)
    return jsonify(response)


@app.route('/custom', methods=['POST'])
def custom():
    data = response_format()
    try:
        request_json = request.get_json(silent=True, force=True)
        if request_json.get('id') is None and request_json.get('image'):
            raise Exception("misisng")
        # print(request_json)
        with open(STATIC_IMAGE_PATH + request_json['id']+request_json['ext'], "wb") as vid:
            image = base64.b64decode(request_json['image'].partition(",")[2])
            vid.write(image)
    except Exception as e:
        print(e)
    # print(request_json)
    response = dict()
    response["status_code"] = 200
    response["data"] = response_format()
    return jsonify(response)


@app.route('/like', methods=['POST'])
def like():
    try:
        request_json = request.get_json(silent=True, force=True)
        if request_json.get('image_id') is None and request_json.get('suggestion_id'):
            raise Exception("missing")
        print(request_json.get('image_id'), request_json.get('suggestion_id'))
    except Exception as e:
        print(e)
    # print(request_json)
    response = dict()
    response["status_code"] = 200
    response["data"] = response_format()
    return jsonify(response)
