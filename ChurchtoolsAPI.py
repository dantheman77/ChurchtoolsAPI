# external imports
import requests
import json

# Project related imports
import sys
sys.path.append("./config")
import churchToolsPropertyReader

# Global
ctProperties = churchToolsPropertyReader.ChurchtoolsPropertyReader("./config/ct.properties")

class ChurchToolsAPI():    
    def __init__(self):
        self.session = requests.Session()
        self.sessionCreated = False

    # Returns the song for the given name
    def findSongByName(self,name):
        url = ctProperties.getRestProperty("churchtools.rest.url.song") + "?name=" + name.replace(" ", "%20")
        return self.__getRequest(url).content

    # Returns the song for the given id
    def findSongById(self,id):
        url = ctProperties.getRestProperty("churchtools.rest.url.song") + "?ids%5B%5D=" + id
        return self.__getRequest(url).content

    # Returns the standard arrangement for a song with the given song id
    def findStandardArrangementBySongId(self, id):
        arrangements = json.loads(self.findSongById(id))["data"][0]["arrangements"]

        for arrangement in arrangements:
            if arrangement["name"].__eq__("Standard-Arrangement"):
                return arrangement

        return null
    
    # Returns the standard arrangement for a song with the given song name
    def findStandardArrangementBySongName(self, name):
        arrangements = json.loads(self.findSongByName(name))["data"][0]["arrangements"]

        for arrangement in arrangements:
            if arrangement["name"].__eq__("Standard-Arrangement"):
                return arrangement

        return null

    # Edit the arrangement key for the specified song id
    def editArrangementKeyForSongName(self, id, keyOfArrangement):
        url = ctProperties.getAjaxProperty("churchtools.ajax.url.churchservice")
        
        arrangement = self.findStandardArrangementBySongId(id)
        arrangement["func"] = "editArrangement"
        arrangement["keyOfArrangement"] = keyOfArrangement

        # Mandatory parameters which are specifically requested by the API     
        arrangement["bezeichnung"] = arrangement["name"]
        arrangement["tonality"] = keyOfArrangement
        arrangement["length_min"] = "0"
        arrangement["length_sec"] = "0"

        print("Update song: " + name + " with key: " + keyOfArrangement)

        response = self.__postRequest(url, arrangement)

        print(response.content)

        return arrangement

    # Edit the arrangement key for the specified song name
    def editArrangementKeyForSongName(self, name, keyOfArrangement):
        url = ctProperties.getAjaxProperty("churchtools.ajax.url.churchservice")
        
        arrangement = self.findStandardArrangementBySongName(name)
        arrangement["func"] = "editArrangement"
        arrangement["keyOfArrangement"] = keyOfArrangement

        # Mandatory parameters     
        arrangement["bezeichnung"] = arrangement["name"]
        arrangement["tonality"] = keyOfArrangement
        arrangement["length_min"] = "0"
        arrangement["length_sec"] = "0"

        print("Update song: " + name + " with key: " + keyOfArrangement)

        response = self.__postRequest(url, arrangement)

        print(response.content)

        return arrangement

    def __getRequest(self, url):
        if self.sessionCreated == False:
            self.__createSession()
        
        return self.session.get(url)

    def __postRequest(self, url, body):
        if self.sessionCreated == False:
            self.__createSession()
        
        return self.session.post(url, json=body)
    
    # Executes login for the churchtoolsAPI
    # APIv1 (Ajax) and APIv2 (Rest) can both be used with this session
    def __createSession(self):
        body = {
            "username":ctProperties.getLoginProperty("churchtools.login.username"),
            "password":ctProperties.getLoginProperty("churchtools.login.password"),
            "rememberMe":False
        }

        loginUrl = ctProperties.getLoginProperty("churchtools.login.rest.url")

        response = self.session.post(loginUrl, json=body)

        if response.status_code == 200:
            self.sessionCreated = True
            return response
        
        self.sessionCreated = False
        return null

