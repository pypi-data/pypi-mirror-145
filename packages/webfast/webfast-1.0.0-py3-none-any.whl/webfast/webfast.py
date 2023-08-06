"""
    (c) 2022 Rodney Maniego Jr.
    WebFast
"""

import shlex
from namari import Namari
from arkivist import Arkivist
from wbuilder import WebBuilder
from wbuilder import wbuilder

class WebFast:
    def __init__(self, filepath=None):
        self.filepath = None
        self.rels = Namari()
        self.selectors = Arkivist()
        self.Html5Tags = wbuilder._getHtml5Tags()
        self.Html5Properties = wbuilder._getProperties()
        if isinstance(filepath, str):
            self.filepath = filepath
        self.autoWbIDs = []

    def  __setitem__(self, selector, ftml):
        properties = _decodeFtml(ftml, self.Html5Tags, self.Html5Properties)
        if isinstance(selector, str) and len(properties):
            if "id" not in properties:
                id = wbuilder._newId()
                self.autoWbIDs.append(id)
                properties.set("id", id)
            self.rels.set(selector, properties["id"])
            self.selectors.update({properties["id"]: properties})
    
    def  __getitem__(self, selector):
        if selector in self.selectors:
            return self[selector]
    
    def build(self):
        used = []
        json = {}
        for selector, children in self.rels.items():
            for child in children:
                used.append(child)
                attribs = self.selectors[child]
                attribs["id"] = child
                attribs["selector"] = selector
                json.update({len(json): attribs})
        for selector, attribs in self.selectors.items():
            if selector not in used:
                if len(attribs) > 0:
                    attribs["id"] = selector
                    attribs["selector"] = selector
                    json.update({len(json): attribs})
        html = WebBuilder()
        html.autoWbIDs = self.autoWbIDs
        html.fromJson(json)
        return html.build()

def _decodeFtml(ftml, Html5Tags, Html5Properties):
    # "div #id.class1.class2.class3 data-var='hello' style='font-size:20px;color:#000;' > hello, world!"
    properties = Arkivist()
    if isinstance(ftml, str):
        temp = list(ftml.split(">"))
        ftml = temp[0].strip()
        if len(temp) == 2:
            properties["html"] = temp[1].strip()
        tag = list(ftml.split(" "))[0].strip()
        if tag not in Html5Tags:
            return properties
        properties["tag"] = tag
        ftml = " ".join(list(ftml.split(" "))[1:])
        for part in shlex.split(ftml):
            if len(part:=part.strip()):
                temp = list(part.split("="))
                name = temp[0]
                value = ""
                if len(temp) == 2:
                    value = temp[1].strip()
                if (name in Html5Properties) or ("data-" in name):
                    properties[name] = value
                else:
                    part = part.replace(".", " .")
                    for id in part.split(" "):
                        if "#" in id:
                            properties.set("id", id.strip())
                        else:
                            properties.appendIn("class", id.strip())
        
        options = {"escape": True, "static": False, "cached": True}
        for property, value in options.items():
            if property not in properties:
                properties[property] = value
    return properties