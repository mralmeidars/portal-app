from portal.services import mongoDatabase as db
from portal.services import cleanData
from urllib.parse import urlparse
from lxml import html as lxml_html
from json import load as json_load

import datetime     as dt
import googlesearch as gs
import requests     as req

_dtGoogle = {}

def getContent(_url):
    res = req.get(_url, timeout=30)
    if res.status_code == 200:
        return res.content
    else:
        return ' '

class googleClient(object):

    def getData(self):
        with open('portal/static/parameters.json') as params:
            __params = json_load(params)

        _dtGoogle[__params['GOOGLE_DB_COLLECTION']] = []
        __countDomains = 0

        __dbData = db.mongoData()

        for __url in gs.search(query=__params['TRACKING_TERM'], lang='pt', stop=150, pause=1):
            try:
                # Get Content
                __content = getContent(__url)

                # Get just texts from Content
                __htmlElements = lxml_html.document_fromstring(__content)    
                __allElements  = __htmlElements.cssselect('div')

                __htmlContent  = ' '
                __htmlContent  = [__htmlContent + ' ' + elem.text_content() for elem in __allElements]
                __htmlContent  = str(__htmlContent).lower()

                # Cleaning Data
                __htmlContent = cleanData.cleanEmoji(__htmlContent)
                __htmlContent = cleanData.cleanText(__htmlContent)

                # Get Domain from URL
                __parseDomain = urlparse(__url)
                __domain      = str(__parseDomain.netloc)
                __domain      = __domain.replace('http://','').replace('https://','').replace('www.','')

            except Exception:
                __domain      = ' '
                __htmlContent = ' '
                pass

            # if valid Domain
            if not (__domain == ' '):
                __countDomains += 1

                # Create Dictionary
                appendData = {'url': __url, 'domain': __domain, 'content': __htmlContent}
                _dtGoogle['google'].append(appendData)

            if (__countDomains == __params['GOOGLE_LIMIT_SEARCH']):
                break

        # Storage Data
        __dbData.addManyData(   __params['MONGO_DB'],
                                __params['GOOGLE_DB_COLLECTION'],
                                _dtGoogle[__params['GOOGLE_DB_COLLECTION']])
