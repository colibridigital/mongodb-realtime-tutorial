import pymongo
import os

# Define Mongo Connection Details
mongo_username = os.environ['MONGODB_USERNAME']
mongo_password = os.environ['MONGODB_PASSWORD']
mongo_uri = "mongodb+srv://sandbox.nupbd.mongodb.net"

# Establish Connection
client = pymongo.MongoClient(
    mongo_uri, username=mongo_username, password=mongo_password)

# Only get two fields for Florida
pipeline = [
    {'$project': {'fullDocument': 1, 'operationType': 1}},
    {'$match': {'fullDocument.statistical_area_state': 'FL Metro Area'}}
]

# Connect to Database
db = client.sandbox

# Attach pipeline to collection
cursor = db.uspopulation.watch(pipeline=pipeline)

# Start Change Stream
while(True):
    document = next(cursor)

    if document['operationType'] in ["insert", "replace"]:
        print("An operation of type {0} has occured.".format(
            document['operationType']))
        print("The new document is: {0}".format(
            document))
