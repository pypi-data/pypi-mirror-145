"""
    Copyright (C) 2022  Emojipypi

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    The full license term can be found at the root directory
    of this project. If not, refer to https://github.com/Emojigit/mw.
"""

# Metadata
__version__ = "0.0.1"
__author__ = "Emojipypi"

# Imports
import requests
from typing import Union, Iterable


"""
    The holy MediaWiki API Error object.
    All other API exceptions should be its child.
"""
class MWAPIError(Exception):
    def __init__(self,dump:dict = {},message: Union[str,None] = None):
        try:
            self.dump = dump
            errors = dump["errors"] if "errors" in dump else [] # In case of strange error handler like MWLoginError
            error_list = []
            for x in errors:
                error_list.append(x["code"])
            self.codes = error_list
            if message == None:
                if len(errors) == 1:
                    self.message = errors[0]["text"] if "text" in errors[0] else errors[0]["*"] if "*" in errors[0] else ""
                else:
                    self.message = "{} errors generated: {}".format(len(errors),", ".join(self.codes))
            else:
                self.message = message
            super().__init__(self.message)
        except:
            # In case we have ANY error, we can still get the dump as debug
            print(dump)
            raise


class MWLoginError(MWAPIError):
    def __init__(self,message: str,dump:dict = {}):
        self.message = "Login Failed: {}".format(message)
        super().__init__(dump,self.message)

class MWEditError(MWAPIError):
    pass

"""
    A callable string!
    You can get the result
    by treatig them as normal strings
    or calling them.
"""
class CallableString(str):
    def __call__(self):
        return self.__str__()

"""
    List of Wikimedia official sites
    They can be accessed by their full name,
    or short form (according to interwiki links),
    or without the "pedia" prefix, if any.
"""
class WMSitesBase:
    # Language Sites
    def wikipedia(self,lang: str):
        return "https://{}.wikipedia.org/w/api.php".format(lang)
    pedia = wikipedia
    wp = wikipedia
    def wiktionary(self,lang: str):
        return "https://{}.wiktionary.org/w/api.php".format(lang)
    tionary = wiktionary
    wikit = wiktionary
    def wikisource(self,lang: str):
        return "https://{}.wikisource.org/w/api.php".format(lang)
    source = wikisource
    s = wikisource
    def wikiquote(self,lang: str):
        return "https://{}.wikiquote.org/w/api.php".format(lang)
    quote = wikiquote
    q = wikiquote
    def wikibooks(self,lang: str):
        return "https://{}.wikiquote.org/w/api.php".format(lang)
    books = wikibooks
    b = wikibooks
    def wikinews(self,lang: str):
        return "https://{}.wikinews.org/w/api.php".format(lang)
    news = wikinews
    n = wikinews
    def wikivoyage(self,lang: str):
        return "https://{}.wikivoyage.org/w/api.php".format(lang)
    voyage = wikivoyage
    voy = wikivoyage
    def wikiversity(self,lang: str):
        return "https://{}.wikiversity.org/w/api.php".format(lang)
    versity = wikiversity
    v = wikiversity
    # Global sites
    wikispecies = CallableString("https://species.wikimedia.org/w/api.php")
    species = wikispecies
    commons = CallableString("https://commons.wikimedia.org/w/api.php")
    wikidata = CallableString("https://www.wikidata.org/w/api.php")
    data = wikidata
    d = wikidata
    mediawiki = CallableString("https://www.mediawiki.org/w/api.php")
    mw = mediawiki
    meta = CallableString("https://meta.wikimedia.org/w/api.php")
WMSites = WMSitesBase()

"""
    Holy API object.
"""
class API:
    def __init__(self,site):
        self.S = requests.Session()
        self.site = site
    def get(self,body: dict):
        req = body.copy()
        req["errorformat"] = "plaintext"
        req["format"] = "json"
        R = self.S.get(url=self.site, params=req)
        DATA = R.json()
        if "errors" in DATA:
            raise MWAPIError(DATA)
        return DATA
    def post(self,body: dict):
        req = body.copy()
        req["errorformat"] = "plaintext"
        req["format"] = "json"
        R = self.S.post(url=self.site, data=req)
        DATA = R.json()
        if "errors" in DATA:
            raise MWAPIError(DATA)
        return DATA
    def token(self,type: str,curtimestamp: bool = False):
        req = {
            "action": "query",
            "meta": "tokens",
            "curtimestamp": curtimestamp,
            "type": type
        }
        DATA = self.get(req)
        return DATA['query']['tokens'][type + "token"], (DATA["curtimestamp"] if curtimestamp else None)
    def csrf(self):
        token, ts = self.token("csrf",True)
        return token, ts
    def logintoken(self):
        return self.token("login")
    def login(self,username: str,botpassword: str):
        token = self.logintoken()
        req = {
            "action": "login",
            "lgname": username,
            "lgpassword": botpassword,
            "lgtoken": token
        }
        DATA = self.post(req)
        if DATA["login"]["result"] != "Success":
            raise MWLoginError(DATA["login"]["result"],DATA)
        return DATA
    def edit(self,page: Union[str,int], content: Union[dict,str], token: Union[str,None] = None, ts: Union[str,bool] = True):
        pageType = "pageid" if isinstance(page,int) else "title"
        req = content.copy() if isinstance(content,dict) else {"text": content}
        tmp_ts = ts
        if token == None:
            token, tmp_ts = self.csrf()
        if ts == False or ts == "":
            tmp_ts = "now"
        req["token"] = token
        req["starttimestamp"] = tmp_ts
        req["action"] = "edit"
        req[pageType] = page
        DATA = self.post(req)
        if "errors" in DATA:
            raise MWEditError(DATA)
        return DATA

MWAPI = API



