"""
    wBuilder v2.0
    (c) 2020 Rodney Maniego Jr.
    https://github.com/rmaniego/wbuilder
    MIT License
"""

from wbuilder import WebBuilder


class FromJSONBuild:
    def __init__(self, json, document=None):
        self.json = None
        if isinstance(json, dict):
            self.json = json
        self.document = None
        if isinstance(document, str):
            self.document = document
    
    def append(self, json):
        if isinstance(json, dict):
            self.json.update(json)
        return self
    
    def clear(self):
        self.json = None
        return self
    
    def build(self):
        return parse(self.json)


def parse(json, document):
    document = WebBuilder(html=document)
    for element in json.values():
        tag = json.get("tag", "div")
        Id = json.get("Id", "")
        Class = json.get("Class", "")
        for key, value in element.items():
        
        if json.get("static", "") == "True"
            
            
        