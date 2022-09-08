import configparser

class ChurchtoolsPropertyReader:
    def __init__(self, configpath):
        self.config = configparser.ConfigParser()
        self.config.read(configpath)

    def getLoginProperty(self,propertyName):
        return self.config.get('LoginSection', propertyName)

    def getAjaxProperty(self,propertyName):
        return self.config.get('AjaxSection', propertyName)

    def getRestProperty(self,propertyName):
        return self.config.get('RestSection', propertyName)

