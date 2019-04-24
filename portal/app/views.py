from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from json import dumps as json_dumps
from json import load as json_load

from portal.services import executeThreads
from portal.services import getTweetsPerUser
from portal.services import getTweetsPerWeekday
from portal.services import getTweetsPerHour
from portal.services import getDomainsFrequecy

def home(_request):

    if _request.method == 'POST':
        return redirect ('portal')
    else:
        return render(_request, 'home.html')

def loadPortal(_request):

    worker = executeThreads.scrapingProcess()
    worker.runScraping()

    return redirect ('twitterlists')

def loadDashboardTwitter(_request, _typeReport='lists'):

    # Get Parameters
    with open('portal/static/parameters.json') as params:
        __params = json_load(params)

    # Load Tweets per User
    __tweetsUser = getTweetsPerUser.getData(    _typeReport,
                                                __params['MONGO_DB'],
                                                __params['TWITTER_DB_COLLECTION'] )

    # Load Tweets per Weekday
    __tweetsWeekday = getTweetsPerWeekday.getData(  _typeReport,
                                                    __params['MONGO_DB'],
                                                    __params['TWITTER_DB_COLLECTION'] )

    # Load Tweets per Hour
    __tweetsHour = getTweetsPerHour.getData(    _typeReport,
                                                __params['MONGO_DB'],
                                                __params['TWITTER_DB_COLLECTION'] )

    if (_typeReport == 'lists'):
        __page = _request.GET.get('page', 1)
        __paginator = Paginator(__tweetsUser, 25)
        try:
            __tweetsUser = __paginator.page(__page)
        except PageNotAnInteger:
            __tweetsUser = __paginator.page(1)
        except EmptyPage:
            __tweetsUser = __paginator.page(__paginator.num_pages)

    # Load multiple Contexts
    __context = {'tweetsUser': __tweetsUser if (_typeReport == 'lists') else json_dumps(__tweetsUser)}
    __context.update( {'tweetsWeekday': __tweetsWeekday if (_typeReport == 'lists') else json_dumps(__tweetsWeekday)} )
    __context.update( {'tweetsHour': __tweetsHour} )

    return render(_request, 'twitterLists.html' if (_typeReport == 'lists') else 'twitterGraphs.html', __context)


def loadDashboardGoogle(_request, _typeReport='lists'):

    # Get Parameters
    with open('portal/static/parameters.json') as params:
        __params = json_load(params)

    # Load Domains Frequency
    __domainsFrequency = getDomainsFrequecy.getData(    _typeReport,
                                                        __params['MONGO_DB'],
                                                        __params['GOOGLE_DB_COLLECTION'] )

    if (_typeReport == 'lists'):
        __page = _request.GET.get('page', 1)
        __paginator = Paginator(__domainsFrequency, 25)
        try:
            __domainsFrequency = __paginator.page(__page)
        except PageNotAnInteger:
            __domainsFrequency = __paginator.page(1)
        except EmptyPage:
            __domainsFrequency = __paginator.page(__paginator.num_pages)

    __context = {'domainsFrequency': __domainsFrequency if (_typeReport == 'lists') else json_dumps(__domainsFrequency)}

    return render(_request, 'googleLists.html' if (_typeReport == 'lists') else 'googleGraphs.html', __context)
