## Sam :)
## Created 10-07-21

## ---- gameboxdb.py ----
# 
# Provides methods for accessing the IGDB API.
#
# Requirements:
# - requests
#
## --------------------


import requests, time, requests_oauthlib
from datetime import datetime, timezone

import os

IGDB_BASE_URL = "https://api.igdb.com/v4"

## ---------------------
### Data Access Objects
## ---------------------

class RequestResult():
    def __init__(self, err):
        self.error_code = err

class GameRequestResult(RequestResult):
    def __init__(self, err, id, name):
        RequestResult.__init__(self, err)
        self.id = id
        self.name = name

class GameCoverRequestResult(GameRequestResult):
    def __init__(self, err, id, name, url):
        GameRequestResult.__init__(self, err, id, name)
        self.url = url

## ---------------------
### API Methods
## ---------------------

def GetOAuth2Token(appid, secret):
    requestURL = "https://id.twitch.tv/oauth2/token"
    requestPayload = {
            'client_id': appid,
            'client_secret': secret,
            'grant_type': 'client_credentials'
        }

    apiRequest = requests.post(requestURL, params=requestPayload)
    return apiRequest.json()['access_token']

def SearchGames(token, appid, query):
    requestURL = IGDB_BASE_URL + "/games/"
    requestHeaders = {
            'Authorization': "Bearer " + token,
            'Client-ID': appid,
            'Accept' : 'application/json'
    }
    requestPayload = 'search "' + query + '"; where parent_game = null & version_parent = null; fields id, name; limit 10;'
    
    apiRequest = requests.post(requestURL, headers=requestHeaders, data=requestPayload)
    json = apiRequest.json()

    results = []

    for o in json:
        results.append(GameRequestResult(apiRequest.status_code, o['id'], o['name']))

    return results

def GetGameByURL(token, appid, query):
    requestURL = IGDB_BASE_URL + "/games/"
    requestHeaders = {
            'Authorization': "Bearer " + token,
            'Client-ID': appid,
            'Accept' : 'application/json'
    }
    requestPayload = 'where url = "' + query + '"; fields id, name; limit 11;'
    
    apiRequest = requests.post(requestURL, headers=requestHeaders, data=requestPayload)
    json = apiRequest.json()

    ## TODO - Validate this properly
    return GameRequestResult(apiRequest.status_code, json[0]['id'], json[0]['name'])

def GetGameByID(token, appid, id):
    requestURL = IGDB_BASE_URL + "/games/"
    requestHeaders = {
            'Authorization': "Bearer " + token,
            'Client-ID': appid,
            'Accept' : 'application/json'
    }
    requestPayload = 'where id = ' + str(id) + '; fields id, name; limit 11;'
    
    apiRequest = requests.post(requestURL, headers=requestHeaders, data=requestPayload)
    json = apiRequest.json()

    ## TODO - Validate this properly
    return GameRequestResult(apiRequest.status_code, json[0]['id'], json[0]['name'])

def GetGameCover(token, appid, id):
    requestURL = IGDB_BASE_URL + "/covers/"
    requestHeaders = {
            'Authorization': "Bearer " + token,
            'Client-ID': appid,
            'Accept' : 'application/json'
    }
    requestPayload = 'where game = ' + str(id) + '; fields game,height,image_id,width; limit 1;'
    
    apiRequest = requests.post(requestURL, headers=requestHeaders, data=requestPayload)
    json = apiRequest.json()

    imageURL = "https://images.igdb.com/igdb/image/upload/t_cover_big/" + json[0]['image_id'] + ".jpg"

    game = GetGameByID(token, appid, json[0]['game'])

    return GameCoverRequestResult(apiRequest.status_code, json[0]['game'], game.name, imageURL)

if __name__ == "__main__":
    appid = os.getenv("TWITCHTVAPPID")
    token = GetOAuth2Token(appid, os.getenv("TWITCHTVAPPKEY"))
    searchid = SearchGames(token, appid, "Returnal")
    id = GetGameByURL(token, appid, "https://www.igdb.com/games/returnal")
    print(GetGameCover(token, appid, id))