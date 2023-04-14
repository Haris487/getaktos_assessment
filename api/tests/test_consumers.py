import json
import time

import geojson
from django.test import TestCase
from api.models import Consumer
import csv
import geojson

raw_data = []


class ConsumersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        global raw_data
        with open('api/tests/test_consumers_data.csv') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                consumer = Consumer(
                    id=row[0],
                    street=row[1],
                    status=row[2],
                    previous_jobs_count=row[3],
                    amount_due=row[4],
                    lat=row[5],
                    lng=row[6]
                )
                consumer.save()
                raw_data.append(row)

    def verify_data(self, raw_ids, features):
        global raw_data
        for feature in features:
            raw_data_obj = raw_data[raw_ids.pop(0)]
            assert feature.type == 'Feature'
            assert feature.get('geometry').is_valid
            assert feature.get('geometry').type == 'Point'
            assert len(feature.get('properties')) == 5
            assert feature.get('properties').get('id') == raw_data_obj[0]
            assert feature.get('properties').get('street') == raw_data_obj[1]
            assert feature.get('properties').get('status') == raw_data_obj[2]
            assert feature.get('properties').get('previous_jobs_count') == int(raw_data_obj[3])
            assert feature.get('properties').get('amount_due') == int(raw_data_obj[4])
            assert feature.get('geometry').get('coordinates')[1] == float(format(float(raw_data_obj[5]), ".6f"))
            assert feature.get('geometry').get('coordinates')[0] == float(format(float(raw_data_obj[6]), ".6f"))

    def test_without_filter(self):
        response = self.client.get("/consumers")
        geojson_obj = geojson.loads(response.content)
        assert response.status_code == 200
        assert geojson_obj.is_valid
        assert len(geojson_obj.features) == 11

        ## Should return all data
        self.verify_data([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], geojson_obj.features)

    def test_with_filter1(self):
        response = self.client.get("/consumers?min_previous_jobs_count=2&max_previous_jobs_count=3&status=active")
        geojson_obj = geojson.loads(response.content)
        assert response.status_code == 200
        assert geojson_obj.is_valid
        assert len(geojson_obj.features) == 1

        ## Should return data with id 9 in csv
        self.verify_data([9], geojson_obj.features)

    def test_with_filter_should_not_return_anything(self):
        response = self.client.get("/consumers?previous_jobs_count=3&status=collected")
        geojson_obj = geojson.loads(response.content)
        assert response.status_code == 200
        assert geojson_obj.is_valid
        assert len(geojson_obj.features) == 0

    def test_with_filter3(self):
        response = self.client.get("/consumers?min_previous_jobs_count=2")
        geojson_obj = geojson.loads(response.content)
        assert response.status_code == 200
        assert geojson_obj.is_valid
        assert len(geojson_obj.features) == 4

        ## Should return data with id 1, 3, 9, 10 in csv
        self.verify_data([1, 3, 9, 10], geojson_obj.features)

    def test_with_filter4(self):
        response = self.client.get("/consumers?max_previous_jobs_count=2")
        geojson_obj = geojson.loads(response.content)
        assert response.status_code == 200
        assert geojson_obj.is_valid
        assert len(geojson_obj.features) == 10

        ## Should return data except with id 10 in csv
        self.verify_data([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], geojson_obj.features)

    def test_with_conflicting_filter(self):
        response = self.client.get("/consumers?max_previous_jobs_count=2&previous_jobs_count=3")
        assert response.status_code == 400

    def test_with_filter5(self):
        response = self.client.get("/consumers?status=collected")
        geojson_obj = geojson.loads(response.content)
        assert response.status_code == 200
        assert geojson_obj.is_valid
        assert len(geojson_obj.features) == 5

        ## Should return data with id 0, 2, 5, 6, 7 in csv
        self.verify_data([0, 2, 5, 6, 7], geojson_obj.features)

    def test_with_typo_errors(self):
        response = self.client.get("/consumers?status=collectedd")
        assert response.status_code == 400

    def test_rate_limiting(self):
        for i in range(11):
            if i == 10:
                response = self.client.get("/consumers?status=collected")
                ## That means request is throttled
                assert response.status_code == 429
            else:
                response = self.client.get("/consumers?status=collected")
                assert response.status_code == 200
        time.sleep(2)

