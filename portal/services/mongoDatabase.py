import pymongo as pm

class mongoData(object):

	def addManyData(self, _database, _collection, _data):
		dbClient = pm.MongoClient('localhost', 27017)
		dbData   = dbClient[_database]
		colData  = dbData[_collection]

		colData.drop()
		colData.insert_many(_data)

	def findData(self, _database, _collection, _query):
		dbClient = pm.MongoClient('localhost', 27017)
		dbData   = dbClient[_database]
		colData  = dbData[_collection]

		return colData.find(_query)

	def agregateData(self, _database, _collection, _query):
		dbClient = pm.MongoClient('localhost', 27017)
		dbData   = dbClient[_database]
		colData  = dbData[_collection]

		return colData.aggregate(_query)
