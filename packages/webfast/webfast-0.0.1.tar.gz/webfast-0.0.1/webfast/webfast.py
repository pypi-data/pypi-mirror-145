"""
    (c) 2022 Rodney Maniego Jr.
    WebFast
"""

import re
from arkivist import Arkivist
from wbuilder import WebBuilder
from wbuilder import _getHtml5Tags

class WebFast:
    def __init__(self, filepath):
        self.filepath = None
        self.Html5Tags = _getHtml5Tags()
        if isinstance(filepath, str):
            self.filepath = filepath
        
    
    def  __setitem__(self, parent, fthml):
        properties = _decodeFtml(ftml, self.Html5Tags)
        if len(properties):
            pass
    
    def  __getitem__(self, ftml):
        return self[fthml]

def _decodeFtml(ftml, Html5Tags):
    # "div #id class='class1 class2 class3' data-var='hello' style='font-size:20px;color:#000;' hello, world!"
    properties = Arkivist()
    if isinstance(ftml, str):
        tag = list(ftml.split(" "))[0]
        if tag not in Html5Tags:
            return properties
        ftml = " ".join(list(ftml.split(" "))[1:-1])
        
        temp = list(ftml.split("&&"))
        ftml = temp[0]
        if len(temp) == 2:
            properties["content"] = temp[1]
        
        