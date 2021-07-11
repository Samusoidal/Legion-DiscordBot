## Sam :)
## Created 10-07-21

## ---- tzsucks.py ----
# 
# Provides methods for accessing timezonedb's API.
#
# Requirements:
# - requests
#
## --------------------


import requests, time
from datetime import datetime, timezone

TZDB_BASE_URL = "http://api.timezonedb.com/v2.1"

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
### API Methods
## ---------------------

def ListAllTimeZones(key):
    requestURL = TZDB_BASE_URL + "/list-time-zone"
    requestPayload = {
            'key': key,
            'format': 'json',
            'fields': 'zoneName,dst,gmtOffset'
        }

    apiRequest = requests.get(requestURL, params=requestPayload)
    print(apiRequest.text)

def GetTimeZone(key, abbreviation):
    requestURL = TZDB_BASE_URL + "/get-time-zone"
    requestPayload = {
            'key': key,
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
    requestURL = TZDB_BASE_URL + "/convert-time-zone"

    requestPayload = {
            'key': key,
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
    print("No Tests Available")