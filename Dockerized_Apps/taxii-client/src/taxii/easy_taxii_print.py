import pprint
from taxii2client.v21 import Server, ApiRoot, Collection, as_pages


def print_api_roots(path, username=None, user_password=None):
    """Prints all api roots in the server
    username and password requirements are dependent on the server"""
    if not username and user_password:
        server1 = Server(url=path)
    else:
        server1 = Server(url=path, user=username, password=user_password)

    print("Server Title: {}".format(server1.title))
    print("Server Description: {}".format(server1.description))
    print("Server Contact: {}".format(server1.contact))
    print("Server Default API: {}\n".format(server1.default.url))

    for api_root in server1.api_roots:
        print("API Title: " + api_root.title)
        print("API Description: {}".format(api_root.description))
        print("API Versions: {}".format(api_root.versions))
        print("API required length: {}".format(api_root.max_content_length))
        print("API URL: {} \n".format(api_root.url))


def print_single_api_root(api_path, username=None, user_password=None):
    """Prints an api root in the server
    username and password requirements are dependent on the server"""
    if not username and user_password:
        api_root = ApiRoot(url=api_path)
    else:
        api_root = ApiRoot(url=api_path, user=username, password=user_password)

    print("API Title: " + api_root.title)
    print("API Description: {}".format(api_root.description))
    print("API Versions: {}".format(api_root.versions))
    print("API required length: {}".format(api_root.max_content_length))
    print("API URL: {} \n".format(api_root.url))


def print_collections_per_api_root(path, username=None, user_password=None):
    """Prints all collections within all api roots in the server
    username and password requirements are dependent on the server"""
    if not username and user_password:
        server1 = Server(url=path)
    else:
        server1 = Server(url=path, user=username, password=user_password)

    for api_root in server1.api_roots:
        print("API Root: {}".format(api_root.title))
        for collection in api_root.collections:
            print("\tTitle: " + collection.title)
            print("\tID: " + collection.id)
            print("\tDescription: {}".format(collection.description))
            print("\tReadable: {}".format(collection.can_read))
            print("\tWriteable: {}".format(collection.can_write))
            print("\tMedia Types: {}".format(collection.media_types))
            print("\tURL: {}".format(collection.url))
            for key, values in collection.custom_properties.items():
                print("\t{}: {}".format(key,values))
            print("\n")


def print_single_collection(collection_path, username=None, user_password=None):
    """Prints a collection within an api root in the server
    username and password requirements are dependent on the server"""
    if not username and user_password:
        collection = Collection(url=collection_path)
    else:
        collection = Collection(url=collection_path, user=username, password=user_password)

    print("\tTitle: " + collection.title)
    print("\tID: " + collection.id)
    print("\tDescription: {}".format(collection.description))
    print("\tReadable: {}".format(collection.can_read))
    print("\tWriteable: {}".format(collection.can_write))
    print("\tMedia Types: {}".format(collection.media_types))
    print("\tURL: {}\n".format(collection.url))


def print_bundles_per_collections_per_api_root(path, username=None, user_password=None):
    """Prints all bundles within each collection within each api roots in the server"""
    if not username and user_password:
        server1 = Server(url=path)
    else:
        server1 = Server(url=path, user=username, password=user_password)
    for api_root in server1.api_roots:
        print("API Root: {}".format(api_root.title))
        for collection in api_root.collections:
            print("\tTitle: " + collection.title)
            print("\tID: " + collection.id)
            if collection.can_read:
                bundle = collection.get_objects()
                pprint.pprint(bundle)
            else:
                print("\tCannot access")


def print_bundles_per_single_collection(collection_path, username=None, user_password=None):
    """Prints all bundles within a collection in the server
    username and password requirements are dependent on the server"""
    if not username and user_password:
        collection = Collection(url=collection_path)
    else:
        collection = Collection(url=collection_path, user=username, password=user_password)

    print("\tTitle: " + collection.title)
    print("\tID: " + collection.id)
    print("\tDescription: {}".format(collection.description))
    print("\tReadable: {}".format(collection.can_read))
    print("\tWriteable: {}".format(collection.can_write))
    print("\tMedia Types: {}".format(collection.media_types))
    print("\tURL: {}\n".format(collection.url))
    if collection.can_read:
        bundle = collection.get_objects()
        pprint.pprint(bundle)
    else:
        print("\tCannot access")


def print_single_object(collection_path, object_id, username=None, user_password=None):
    """Prints a single object in a collections
     username and password requirements are dependent on the server"""
    if not username and user_password:
        collection = Collection(url=collection_path)
    else:
        collection = Collection(url=collection_path, user=username, password=user_password)

    bundle = collection.get_object(object_id)
    print("\tTitle: " + collection.title)
    print("\tID: " + collection.id)
    print("\t===============Object=============")
    pprint.pprint(bundle)
    object_list = bundle["objects"]
    for obj in object_list:
        print(obj)


def print_manifest_per_collections_per_api_root(path, username=None, user_password=None):
    """Prints all manifests within each collection within each api root in the server
    username and password requirements are dependent on the server"""
    if not username and user_password:
        server1 = Server(url=path)
    else:
        server1 = Server(url=path, user=username, password=user_password)
    for api_root in server1.api_roots:
        print("API Root: {}".format(api_root.title))
        for collection in api_root.collections:
            print("\tTitle: " + collection.title)
            print("\tID: " + collection.id)
            if collection.can_read:
                try:
                    manifest_resource = collection.get_manifest()
                    pprint.pprint(manifest_resource)
                except:
                    pass
            else:
                print("\tCannot access")


def print_manifest_per_single_collection(collection_path, username=None, user_password=None):
    """Prints all manifests within a collection
    username and password requirements are dependent on the server"""
    if not username and user_password:
        collection = Collection(url=collection_path)
    else:
        collection = Collection(url=collection_path, user=username, password=user_password)

    print("\tTitle: " + collection.title)
    print("\tID: " + collection.id)
    print("\tDescription: {}".format(collection.description))
    print("\tReadable: {}".format(collection.can_read))
    print("\tWriteable: {}".format(collection.can_write))
    print("\tMedia Types: {}".format(collection.media_types))
    print("\tURL: {}\n".format(collection.url))
    if collection.can_read:
        bundle = collection.get_manifest()
        pprint.pprint(bundle)
    else:
        print("\tCannot access")


def copy_object_to_collection(from_collection_path, to_collection_path, object_id, from_username=None, from_user_password=None, to_username=None, to_user_password=None):
    """copies bundle from one collection to another collection
    username and password requirements are dependent on the server"""
    if not from_username and from_user_password:
        from_collection = Collection(url=from_collection_path)
    else:
        from_collection = Collection(url=from_collection_path, user=from_username, password=from_user_password)

    if not to_username and to_username:
        to_collection = Collection(url=to_collection_path)
    else:
        to_collection = Collection(url=to_collection_path, user=to_username, password=to_user_password)

    bundle = from_collection.get_object(object_id)
    to_collection.add_objects(bundle)
    print("========Successful===========")
    to_collection.get_object(bundle)
    # try:
    #     bundle = from_collection.get_object(object_id)
    #     to_collection.add_objects(bundle)
    #     print("========Successful===========")
    #     to_collection.get_object(bundle)
    # except:
    #     print("Addition Failed")