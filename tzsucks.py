## Sam :)
## Created 10-07-21

## ---- tzsucks.py ----
# 
# Provides methods for accessing timezonedb's API.
#
# Requirements:
# - requests
# - timezonedb API key, stored as env var 'TIMEZONEDBKEY'
#
## --------------------


import requests, os, time
from datetime import datetime, timezone


## ---------------------
### Data Access Objects
## ---------------------

class RequestResult():
    def __init__(self, err):
        self.error_code = err

class TimeZoneRequestResult(RequestResult):
    def __init__(self, err, tmstmp, abbrev, gmtoff):
        RequestResult.__init__(self, err)
        self.timestamp = tmstmp
        self.abbreviation = abbrev
        self.gmtOffset = gmtoff
        self.formatted = datetime.fromtimestamp(tmstmp, timezone.utc)

class TimeZoneConvertRequestResult(TimeZoneRequestResult):
    def __init__(self, err, tmstmp, abbrev, gmtoff, tmstmp2, abbrev2):
        TimeZoneRequestResult.__init__(self, err, tmstmp, abbrev, gmtoff)
        self.fromTimestamp = tmstmp2
        self.fromAbbreviation = abbrev2
        self.fromFormatted = datetime.fromtimestamp(tmstmp2, timezone.utc)


## ---------------------
### Utility Methods
## ---------------------

def GetAPIKey():
    return os.getenv('TIMEZONEDBKEY');


## ---------------------
### API Methods
## ---------------------

def ListAllTimeZones():
    requestURL = "http://api.timezonedb.com/v2.1/list-time-zone"
    requestPayload = {
            'key': GetAPIKey(),
            'format': 'json',
            'fields': 'zoneName,dst,gmtOffset'
        }

    apiRequest = requests.get(requestURL, params=requestPayload)
    print(apiRequest.text)

def GetTimeZone(abbreviation):
    requestURL = "http://api.timezonedb.com/v2.1/get-time-zone"
    requestPayload = {
            'key': GetAPIKey(),
            'format': 'json',
            'fields': 'zoneName,dst,gmtOffset,timestamp',
            'by': 'zone',
            'zone': abbreviation
        }

    apiRequest = requests.get(requestURL, params=requestPayload)
    apiRequestResults = apiRequest.json()
    resultTimestampFormatted = time.strftime('%H:%M:%S', time.gmtime(apiRequestResults['timestamp']))
    
    resultDAO = TimeZoneRequestResult(apiRequest.status_code,apiRequestResults['timestamp'], abbreviation, apiRequestResults['gmtOffset'])
    return resultDAO

def ConvertTimeZone(timezoneFrom, timezoneTo, localtime=None):
    requestURL = "http://api.timezonedb.com/v2.1/convert-time-zone"

    requestPayload = {
            'key': GetAPIKey(),
            'format': 'json',
            'fields': 'fromZoneName,toZoneName,offset,fromTimestamp,toTimestamp',
            'from': timezoneFrom,
            'to': timezoneTo
        }

    if localtime != None:
        requestPayload['time'] = localtime

    apiRequest = requests.get(requestURL, params=requestPayload)
    apiRequestResults = apiRequest.json()

    resultTimestampFormatted = time.strftime('%H:%M:%S', time.gmtime(apiRequestResults['toTimestamp']))
    
    resultDAO = TimeZoneConvertRequestResult(apiRequest.status_code,apiRequestResults['toTimestamp'], timezoneFrom, apiRequestResults['offset'], apiRequestResults['fromTimestamp'], timezoneTo)

    return resultDAO

if __name__ == "__main__":
    r = GetTimeZone("EST")
    print(datetime.fromtimestamp(r.timestamp, timezone.utc))