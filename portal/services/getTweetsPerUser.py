from portal.services import mongoDatabase as db

def getData(_typeReport, _databaseName, _collectionName):

    __dbData = db.mongoData()

    __pipeline = [  {'$group':{'_id':{'user':'$user'},'countTweets':{'$sum':1}}},
                    {'$sort':{'countTweets':-1,'user':1}},
                    {'$limit':50},
                    {'$project':{'user':'$_id.user','countTweets':1}}]

    __resultData = list(__dbData.agregateData(_database=_databaseName, _collection=_collectionName, _query=__pipeline))

    if (_typeReport == 'graphs'):
        __resultData = [[item['user'],item['countTweets'],] for item in __resultData]

    return __resultData
