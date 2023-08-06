# -*- coding: utf-8 -*-
from efr.utils import singleton

class INFORMODE:...
class MODEDIR(INFORMODE):...
class MODEFILE(INFORMODE):...


class InforNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.kids = []
    def addKid(self, kid:InforNode):
        if kid.parent:
            kid.parent.remove(self)




class PlugInfor(InforNode):  # root
    """
    mod的打包/解包配置
    """
    def __init__(self, *args, **kwargs):
        self.config(*args, **kwargs)

    def config(self):
        ...

    def setPackMode(self, mode:INFORMODE=MODEDIR):
        ...

    def setPath(self, path:str=""):
        ...

    def setPath(self, path:str=""):
        ...
