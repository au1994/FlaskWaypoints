import json

from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.son import SON
from flask import Flask, request, Response
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = "hiking_trails"
mongo = PyMongo(app, config_prefix='MONGO')

def toJson(data):
    return json.dumps(data, default=json_util.default)


@app.route('/trails/create', methods=['POST'])
def create_trail():
    print request.get_data()
    print type(request.get_json())
    trails = mongo.db.trails
    trail_id = trails.insert_one(request.get_json()).inserted_id
    response  = {}
    response["result"] = "success"
    response["trailId"] = str(trail_id)
    data = toJson(response)
    return Response(data, status=200, mimetype='application/json')

@app.route('/trails/get/<trailid>', methods=['GET'])
def get_trail(trailid):
    trails = mongo.db.trails
    trail = trails.find_one({"_id": ObjectId(trailid)})
    print trail
    print type(trail)
    import pdb; pdb.set_trace()
    data = toJson(trail)
    return Response(data, status=200, content_type='application/json')

@app.route('/trails/search', methods=['GET'])
def search_trail():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    lat = float(lat)
    lon = float(lon)
    print type(lat)
    print "from print %s" %lat
    query = {"startingPoint":
                { "$near" :
                    {
                        "$geometry": { "type": "Point", "coordinates": [ lat, lon ] },
                        "$minDistance": 0,
                        "$maxDistance": 10000
                    }
                }
            }
    result = mongo.db.trails.find(query);
    #import pdb; pdb.set_trace()
    print result.count()
    data = dumps(result)

    return Response(data, status=200, content_type='application/json')
        
if __name__ == '__main__':
    app.run()
