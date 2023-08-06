from pythontools.core import tools
from pythontools.dev import crypthography
import os, json

cfg = None


class Config:

    def __init__(self, path="", default_config={}, file_name="config.json"):
        self.default_config = default_config
        if "%APPDATA%" in path:
            path = path.replace("%APPDATA%", str(os.getenv("APPDATA")))
        self.path = os.path.join(path, file_name)
        dir_name = os.path.dirname(self.path)
        if dir_name not in ["", "/"] and not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        self.reloadConfig()

    def reloadConfig(self):
        if not os.path.isfile(self.path):
            tools.createFile(self.path)
            tools.saveJson(self.path, self.default_config, indent=4)
        self.config = tools.loadJson(self.path)
        global cfg
        cfg = self

    def getConfig(self):
        return self.config

    def saveConfig(self):
        tools.saveJson(self.path, self.config, indent=4)


class EncryptedConfig(Config):

    def __init__(self, secret_key, path="", default_config={}, file_name="config.cfg"):
        self.secret_key = secret_key
        super(EncryptedConfig, self).__init__(path, default_config, file_name)

    def reloadConfig(self):
        if not os.path.isfile(self.path):
            tools.createFile(self.path)
            encrypted = crypthography.encrypt(self.secret_key, json.dumps(self.default_config))
            tools.writeToFile(self.path, encrypted)
        decrypted = crypthography.decrypt(self.secret_key, tools.getFileContent(self.path, asBytes=True))
        self.config = json.loads(decrypted.decode("utf-8"))
        global cfg
        cfg = self

    def saveConfig(self):
        encrypted = crypthography.encrypt(self.secret_key, json.dumps(self.config))
        tools.writeToFile(self.path, encrypted)


def setConfig(config):
    global cfg
    cfg = config


def getConfig():
    global cfg
    return cfg