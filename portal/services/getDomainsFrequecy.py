from portal.services import mongoDatabase as db

def getData(_typeReport, _databaseName, _collectionName):

    __dbData = db.mongoData()

    __pipeline = [  {'$group':{'_id':{'domain':'$domain'},'countDomains':{'$sum':1}}},
                    {'$sort':{'countDomains':-1,'domain':1}},
                    {'$limit':50},
                    {'$project':{'domain':'$_id.domain','countDomains':1}} ]

    __resultData = list(__dbData.agregateData(_database=_databaseName, _collection=_collectionName, _query=__pipeline))

    if (_typeReport == 'graphs'):
        __resultData = [[item['domain'],item['countDomains'],] for item in __resultData]

    return __resultData
