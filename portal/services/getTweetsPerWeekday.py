from portal.services import mongoDatabase as db

def getData(_typeReport, _databaseName, _collectionName):

    __dbData = db.mongoData()

    __pipeline = [ {'$group':{'_id':{'dayOfWeek':{'$dayOfWeek':'$datetime'}},'countTweets':{'$sum':1}}},
                    {'$sort':{'_id':1}},
                    {'$project':{'dayOfWeekDesc':{'$cond':[{'$eq':['$_id.dayOfWeek',1]},'Sunday',
                                                 {'$cond':[{'$eq':['$_id.dayOfWeek',2]},'Monday',
                                                 {'$cond':[{'$eq':['$_id.dayOfWeek',3]},'Tuesday',
                                                 {'$cond':[{'$eq':['$_id.dayOfWeek',4]},'Wednesday',
                                                 {'$cond':[{'$eq':['$_id.dayOfWeek',5]},'Thursday',
                                                 {'$cond':[{'$eq':['$_id.dayOfWeek',6]},'Friday', 'Saturday']}]}]}]}]}]},'countTweets':1 }} ]

    __resultData = list(__dbData.agregateData(_database=_databaseName, _collection=_collectionName, _query=__pipeline))

    if (_typeReport == 'graphs'):
        __resultData = [[item['dayOfWeekDesc'],item['countTweets'],] for item in __resultData]

    return __resultData
