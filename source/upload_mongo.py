from pymongo import MongoClient
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb+srv://studyandshare:study4ever@cluster0-6yb0z.mongodb.net/test?retryWrites=true&w=majority')
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)