from file_management_app.serializers import ItemSerializer, ImportSerializer

# Create your tests here.
from django.test import TestCase



class TestFoo(TestCase):
    def test_serializer(self):
        serializer = ImportSerializer()
        serializer.create(
            {
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
