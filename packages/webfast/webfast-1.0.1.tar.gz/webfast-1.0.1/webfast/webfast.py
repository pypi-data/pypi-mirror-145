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
        self.CSS3Attributes = wbuilder._getAttributes()
        self.Html5Properties = wbuilder._getProperties()
        if isinstance(filepath, str):
            self.filepath = filepath
        self.autoWbIDs = []

    def  __setitem__(self, selector, ftml):
        properties = _decodeFtml(ftml, self.Html5Tags, self.CSS3Attributes, self.Html5Properties)
        if isinstance(selector, str) and len(properties):
            properties["parent"] = selector
            if properties["selector"] == "?":
                properties["selector"] = selector
            if "id" not in properties:
                if selector == properties["parent"]:
                    self.selectors.update({selector: properties})
                    return
                id = wbuilder._newId()
                self.autoWbIDs.append(id)
                properties.set("id", id)
            if not self.rels.contains(selector):
                self.rels.insert(selector)
            self.rels.attach(selector, properties["id"])
            self.selectors.update({properties["id"]: properties})
    
    def  __getitem__(self, selector):
        if selector in self.selectors:
            return self[selector]
    
    def build(self, htmlpath=None):
        used = []
        json = Arkivist(self.filepath).reset()
        for selector, children in self.rels.items():
            for child in children:
                used.append(child)
                attribs = self.selectors[child]
                json.set(json.count(), attribs)
        for selector, attribs in self.selectors.items():
            if selector not in used:
                json.set(json.count(), attribs)
        if not isinstance(htmlpath, str):
            htmlpath = None
        html = WebBuilder(self.filepath)
        html.rels = self.rels
        html.autoWbIDs = self.autoWbIDs
        html.fromJson(json.show())
        return html.build()

def _decodeFtml(ftml, Html5Tags, CSS3Attributes, Html5Properties):
    # "div #id.class1.class2.class3 data-var='hello' style='font-size:20px;color:#000;' > hello, world!"
    properties = Arkivist()
    if isinstance(ftml, str):
        temp = list(ftml.split(">"))
        ftml = temp[0].strip()
        if len(temp) == 2:
            properties["html"] = temp[1].strip()
        tag = list(ftml.split(" "))[0].strip()
        if tag not in Html5Tags:
            properties["selector"] = "?"
        else:
            ftml = " ".join(list(ftml.split(" "))[1:])
            properties["tag"] = tag
        for part in shlex.split(ftml):
            if len(part:=part.strip()):
                temp = list(part.split("="))
                name = temp[0]
                value = ""
                if len(temp) == 2:
                    value = temp[1].strip()
                if (name in Html5Properties) or ("data-" in name):
                    if name == "style":
                        styling = {}
                        for property in value.split(";"):
                            if len(property) > 0:
                                data = property.split(":")
                                if len(data) > 1:
                                    if (key:=data[0].strip()) != "":
                                        if CSS3Attributes.contains(key):
                                            if len((value:=data[1].strip())):
                                                styling.update({key: value})
                        value = styling
                    properties[name] = value
                else:
                    for id in part.split("."):
                        if len(id:=id.strip()):
                            if "#" in id:
                                properties.set("id", id.strip())
                            else:
                                properties.appendIn("class", id)
        
        options = {"escape": True, "static": False, "cached": True}
        for property, value in options.items():
            if property not in properties:
                properties[property] = value
    properties.load(dict(sorted(properties.items())))
    return properties