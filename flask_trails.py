import json
import logging
import traceback

from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.son import SON
from flask import Flask, request, Response
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_DBNAME'] = "hiking_trails"
mongo = PyMongo(app, config_prefix='MONGO')


def connect_db(db_name):
    client = MongoClient()
    db = client[db_name]
    
def drop_db(db_name):
    client = MongoClient()
    client.drop_database(db_name)

def toJson(data):
    return json.dumps(data, default=json_util.default)


@app.route('/trails/create', methods=['POST'])
def create_trail():
    trails = mongo.db.trails
    try:
        trail_id = trails.insert_one(request.get_json()).inserted_id
    except Exception as e:
        response = {}
        response["result"] = "error"
        data = toJson(response)
        traceback.print_exc(e)
        logging.warning(e)
        return Response(data, status=408, mimetype='application/json')

    logging.info(trail_id)
    response = {}
    response["result"] = "success"
    response["trailId"] = str(trail_id)
    data = toJson(response)
    return Response(data, status=200, mimetype='application/json')


@app.route('/trails/get/<trailid>', methods=['GET'])
def get_trail(trailid):
    trails = mongo.db.trails
    status_code = 200
    try:
        response = trails.find_one({"_id": ObjectId(trailid)})
    except Exception as e:
        logging.warning(e)
        traceback.print_exc(e)
        response = {}
        response["result"] = "error"
        status_code = 408

    data = toJson(response)
    return Response(data, status=status_code, content_type='application/json')


@app.route('/trails/search', methods=['GET'])
def search_trail():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    lat = float(lat)
    lon = float(lon)
    logging.info(lat)
    query = {"startingPoint":
                {"$near":
                    {
                        "$geometry": {"type": "Point", "coordinates": [lat, lon]},
                        "$minDistance": 0,
                        "$maxDistance": 10000
                    }
                }
            }
    status_code = 200
    try:
        result = mongo.db.trails.find(query)
    except Exception as e:
        logging.warning(e)
        traceback.print_exc(e)
        result = {}
        result["result"] = "error"
        status_code = 408

    data = dumps(result)

    return Response(data, status=status_code, content_type='application/json')

if __name__ == '__main__':
    app.run()
