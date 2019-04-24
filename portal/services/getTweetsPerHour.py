from portal.services import mongoDatabase as db

def getData(_typeReport, _databaseName, _collectionName):

    __dbData = db.mongoData()

    __pipeline = [  {'$group':{'_id':{'hoursOfDay':{'$hour':'$datetime'}},'countTweets':{'$sum':1}}},
                    {'$sort':{'_id':1}},
                    {'$project':{'hoursOfDay':'$_id.hoursOfDay','countTweets':1}} ]

    __resultData = list(__dbData.agregateData(_database=_databaseName, _collection=_collectionName, _query=__pipeline))

    if (_typeReport == 'graphs'):
        __resultData = [[item['hoursOfDay'],item['countTweets'],] for item in __resultData]

        # Load in Graph Format
        __resultData = [("[{v:[" + str(i[0]) + ",0,0],f:'" + (str(i[0]) if (i[0]<=12) else (str(i[0]-12))) + (" am'}," if (i[0]<12) else " pm'},") + str(i[1]) + "],") for i in __resultData]
        __resultData = str(__resultData).replace('"','').replace(',,',',')

    return __resultData
