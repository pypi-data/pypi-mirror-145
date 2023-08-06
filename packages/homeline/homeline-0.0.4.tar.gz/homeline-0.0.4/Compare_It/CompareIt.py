from multiprocessing import AuthenticationError
import time
import requests
import json

CALLTIMEOUT = 5

class CompareIt:
    _at = ''
    _endpoint = 'https://dev2.mittsmartahus.se/api/0/'
    _username = ''
    _password = ''
    _cachedresponse = {}

    def __init__(self, username, password):
        self._username = username
        self._password = password
        
    def Login(self):
        uri = self._endpoint + 'user/login'
        postbody = {"username": self._username, "password": self._password}
        headers =  {"Content-Type":"application/json"}
        response = requests.post(uri, data=json.dumps(postbody), headers=headers)
        if response.status_code == 200:
            self._at = Util.setAccessToken(response.json()['at'])
            pass
        else:
            raise AuthenticationError("Unable to login")
        
    def GetAllEntities(self):
        uri = self._endpoint + 'view/overview'
        return self._GetCached(uri)

    def GetEntity(self, uuid):
        uri = self._endpoint + 'object/' + uuid
        return self.__GetInternal(uri)

    def _GetCached(self, uri) -> str:
        if uri in self._cachedresponse.keys():
            if time.time() - self._cachedresponse[uri]["dt"] < CALLTIMEOUT:
                return self._cachedresponse[uri]["result"]
        
        return self.__GetInternal(uri)

    def __GetInternal(self, uri):
        if len(self._at) > 1:
            headers =  {"Content-Type":"application/json", "Authorization": self._at}
            response = requests.get(uri, headers = headers)
        else:
            self.Login()
            return self.__GetInternal(uri)

        if response.status_code == 200:
            ret = json.dumps(response.json())
            self._cachedresponse[uri] = {
                "response" : ret,
                "dt": time.time()
            }
            return ret
        else:
            return 'Error!'

    def SetEntity(self, uuid, value):
        uri = self._endpoint + 'object/' + uuid

        if len(self._at) > 1:
            headers =  {"Content-Type":"application/json", "Authorization": self._at}
            body = {"target": value}
            response = requests.put(uri, data=json.dumps(body), headers = headers)
        else:
            self.Login()
            return self.SetEntity(uuid, value)

        if response.status_code == 200:
            pass
        else:
            raise ValueError("Unable to update "+ uuid + " with value: " + value)

class Util:
    @staticmethod
    def setAccessToken(response):
        return 'Bearer ' + response