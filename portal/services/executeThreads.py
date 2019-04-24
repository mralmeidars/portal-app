from portal.services import loadGoogleData as go
from portal.services import loadTwitterData as tw

import threading

def loadGoogle():
    google = go.googleClient()
    google.getData()

def loadTwitter():
    twitter = tw.twitterClient()
    twitter.getData()

class scrapingProcess(object):

    def runScraping(self):
        thrGoogle  = threading.Thread( target=loadGoogle() )
        thrTwitter = threading.Thread( target=loadTwitter() )

        thrGoogle.start()
        thrTwitter.start()

        thrGoogle.join()
        thrTwitter.join()
