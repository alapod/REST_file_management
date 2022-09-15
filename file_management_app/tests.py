from file_management_app.serializers import ItemBatchSerializer, ParentSerializer

# Create your tests here.
from django.test import TestCase

import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
            },
            {
                "type": "FOLDER",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
        ],
        "updateDate": "2022-02-01T12:00:00Z",
    },
    {
        "items": [
            {
                "type": "FILE",
                "url": "/file/url1",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 128,
            },
            {
                "type": "FILE",
                "url": "/file/url2",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 256,
            },
        ],
        "updateDate": "2022-02-02T12:00:00Z",
    },
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
            {
                "type": "FILE",
                "url": "/file/url3",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 512,
            },
            {
                "type": "FILE",
                "url": "/file/url4",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 1024,
            },
        ],
        "updateDate": "2022-02-03T12:00:00Z",
    },
    {
        "items": [
            {
                "type": "FILE",
                "url": "/file/url5",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 64,
            }
        ],
        "updateDate": "2022-02-03T15:00:00Z",
    },
]

API_BASEURL = "http://127.0.0.1:8000/file_management"


class TestFoo(TestCase):
    def test_serializer(self):
        serializer = ItemBatchSerializer(
            data={
                "items": [
                    {
                        "type": "FOLDER",
                        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                        "parentId": None,
                    }
                ],
                "updateDate": "2022-02-01T12:00:00Z",
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

    def request(self, path, method="GET", data=None, json_response=False):
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }
        print("URL:", params["url"])
        if data:
            params["data"] = json.dumps(data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        try:
            print("Sending request")
            print(f"PARAMS: {params}")
            req = urllib.request.Request(**params)
            with urllib.request.urlopen(req) as res:
                print("Decoding")
                res_data = res.read().decode("utf-8")
                if json_response:
                    res_data = json.loads(res_data)
                return (res.getcode(), res_data)
        except urllib.error.HTTPError as e:
            return (e.getcode(), f"{e.fp.read()} {params}")

    """def test_serializer_parent(self):
        serializer = ParentSerializer(data={
                "items": [
                    {
                        "type": "FOLDER",
                        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                        "parentId": 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    }
                ],
                "updateDate": "2022-02-01T12:00:00Z",
            })

        serializer.is_valid(raise_exception=True)
        serializer.save()"""

    def test_import(self):
        for index, batch in enumerate(IMPORT_BATCHES):
            print(f"Importing batch {index}")
            status, response = self.request("/imports", method="POST", data=batch)
            print(response)
            assert status == 200, f"Expected HTTP status code 200, got {status}"

        print("Test import passed.")


a = """{"items":' \
   [{},
   {"parentId":["Invalid pk \\"d515e43f-f3f6-4471-bb77-6b455017a2d2\\" - object does not exist."]},
   {"parentId":["Invalid pk \\"d515e43f-f3f6-4471-bb77-6b455017a2d2\\" - object does not exist."]}
   ]
   }' 
   {'url': 'http://127.0.0.1:8000/file_management/imports', 'method': 'POST', 'headers': {'Content-Length': 467, 'Content-Type': 'application/json'}, 'data': b'{"items": [{"type": "FOLDER", "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2", "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"}, {"type": "FILE", "url": "/file/url1", "id": "863e1a7a-1304-42ae-943b-179184c077e3", "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2", "size": 128}, {"type": "FILE", "url": "/file/url2", "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4", "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2", "size": 256}], "updateDate": "2022-02-02T12:00:00Z"}'}
"""
