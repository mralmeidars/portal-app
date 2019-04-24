from string import digits

import nltk
import unicodedata
import re

def cleanEmoji (_string):
    __patterns = re.compile('['
                          u'\U0001F600-\U0001F64F' # emoticons
                          u'\U0001F300-\U0001F5FF' # symbols & pictographs
                          u'\U0001F680-\U0001F6FF' # transport & map symbols
                          u'\U0001F1E0-\U0001F1FF' # flags (iOS)
                          u'\U00002702-\U000027B0'
                          u'\U000024C2-\U0001F251'
                          u'\U0001f926-\U0001f937'
                          u'\U00010000-\U0010ffff'
                          u'\u200d'
                          u'\u2640-\u2642'
                          u'\u2600-\u2B55'
                          u'\u23cf'
                          u'\u23e9'
                          u'\u231a'
                          u'\u3030'
                          u'\ufe0f'
                           ']+', flags=re.UNICODE)
    
    return __patterns.sub(r'', _string)


def cleanText(_string):

    # Remove quotation marks
    _string = _string.replace("'",'')
    _string = _string.replace('"','')

    # Replace every ('$', ',', ';')
    __regex = re.compile('[$,;]')
    _string = __regex.sub('', _string)

    __regex = re.compile('<.*?>')
    _string = __regex.sub('', _string)

    _string = _string.replace('\\n','')
    _string = _string.replace('\\r','')
    _string = _string.replace('\r','')
    _string = _string.replace('\\t','')
    _string = _string.replace('\\xa0','')

    # Remove numbers
    __removeDigits = str.maketrans('', '', digits)
    _string = _string.translate(__removeDigits)

    # Unicode normalize transforms a character into its Latin equivalent.
    nfkd = unicodedata.normalize('NFKD', _string)
    _string = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return _string

    _string = (' ').join(_string.split())

    return _string
