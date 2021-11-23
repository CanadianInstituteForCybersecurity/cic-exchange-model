Installation Instructions
=========================
1. Run a python virtual environment
2. Install [medallion](https://pypi.org/project/medallion/) and [pymongo](https://pypi.org/project/pymongo/)
2. You can run either a MongoDB backend or a Memory Backend

Running Memory Backend
======================
Run "medallion -config_memory.json"

Running MongoDB Backend
=======================
1. Run initialize_mongodb.py
2. Run "medallion -config_mongodb.json"
