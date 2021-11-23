from taxii2client.v21 import Collection
import requests
from stix2 import TAXIICollectionSink


class TaxiiTransceiver():
    def __init__(self, url, username=None, user_password=None):
        self.url = url
        self.username = username
        self.userpassword = user_password

    def get_single_object(self, collection_id, object_id):
        """Retrieves a single object in a collections
        username and password requirements are dependent on the server"""
        collection_path = self.url + "collections/" + collection_id
        if not self.username and not self.userpassword:
            collection = Collection(url=collection_path)
        else:
            collection = Collection(url=collection_path, user=self.username, password=self.userpassword)

        bundle = collection.get_object(object_id)
        self.object_list = bundle["objects"]

    def get_objects(self, collection_id):
        """Retrieves objects in a collections
        username and password requirements are dependent on the server"""
        collection_path = self.url + "collections/" + collection_id
        if not self.username and not self.userpassword:
            collection = Collection(url=collection_path)
        else:
            collection = Collection(url=collection_path, user=self.username, password=self.userpassword)

        bundle = collection.get_objects()
        return bundle["objects"]


    def add_single_object(self, collection_id, object):
        """Adds a single object in a collections
        username and password requirements are dependent on the server"""
        collection_path = self.url + "collections/" + collection_id
        if not self.username and not self.userpassword:
            collection = Collection(url=collection_path)
        else:
            collection = Collection(url=collection_path, user=self.username, password=self.userpassword)

        taxii_sink = TAXIICollectionSink(collection)
        taxii_sink.add(object)


    def query_dxl(self, url):
        for obj in self.object_list:
            response = requests.post(url=url,json=obj)
            print(response.text)