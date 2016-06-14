import json
import unittest

import pymongo

import flask_trails


class FlaskTrailsTestCase(unittest.TestCase):

    orig_keys = ['trail', '_id', 'userId', 'startingPoint']

    def setUp(self):
        flask_trails.app.config['TESTING'] = True
        flask_trails.connect_db('flask_trails_test_db')

        self.app = flask_trails.app.test_client()

    def tearDown(self):
        flask_trails.drop_db('flask_trails_test_db')

    def test_search_api(self):
        result = self.app.get('/trails/search?lat=28.459497&lon=77.026638')
        data = json.loads(result.data)

        assert type(data) is list

        orig_keys = ['trail', '_id', 'userId', 'startingPoint']
        orig_keys.sort()

        if data:
            for item in data:
                data_item = item
                break
            obj_keys = data_item.keys()
            obj_keys.sort()
            assert obj_keys == orig_keys


if __name__ == "__main__":
    unittest.main()
