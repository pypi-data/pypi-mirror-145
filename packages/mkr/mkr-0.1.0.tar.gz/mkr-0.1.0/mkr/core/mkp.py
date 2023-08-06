# -*- coding: utf-8 -*-
import importlib
import os.path

from files3 import Files

from mkr.utils import *

class MKPState:...
class STATE_RAW(MKPState):...
class STATE_RBUF(MKPState):...
class STATE_RSTRUCT(MKPState):...
class STATE_READY(MKPState):...

class MKPlugInfo:
    def __init__(self, mkplug):
        self.path = mkplug._raw_path
        self.mname = mkplug.mname


class MKPlug:
    STATE_RAW       = STATE_RAW
    STATE_RBUF      = STATE_RBUF
    STATE_RSTRUCT   = STATE_RSTRUCT
    STATE_READY     = STATE_READY
    """
    指定一个'pypackage'，将其加载到当前环境备用
    这个'pypackage'包含__init__.py但其中的import路径按照一个项目的模式来编写
    其__init__.py中需要导入模块所提供的python对象
    共4种状态
    STATE_RAW
        获取到目标path, 尚未初始化
    STATE_RBUF
        已将目标拷贝到mktemp中, 尚未进行重构
    STATE_RSTRUCT
        目标已被重构完毕
    STATE_READY
        目标已经作为mod被成功加载，处于随时可用状态

    """
    def __init__(self, mkpm, mpath:str):
        self.code = None
        self.mkpm = mkpm
        self.packos = mkpm.packos

        assert os.path.isdir(mpath), "dir expected, but got " + mpath
        self._raw_path = mpath  # mod path
        self.path = mpath  # mod path
        self.mname = os.path.basename(self.path)
        self.state = STATE_RAW

    @property
    def raw(self) -> bool:
        return self.state is STATE_RAW

    @property
    def rbuf(self) -> bool:
        return self.state is STATE_RBUF

    @property
    def rstruct(self) -> bool:
        return self.state is STATE_RSTRUCT

    @property
    def ready(self) -> bool:
        return self.state is STATE_READY

    @property
    def pypath(self) -> str:
        return self.mkpm.MKBUFNAME + '.' + self.mname

    @property
    def info(self) -> MKPlugInfo:
        return MKPlugInfo(self)

    def load2buf(self):
        """
        加载野生mod到[buffer]文件夹, 本质上是一个复制操作.
        该操作只能在state为STATE_RAW时进行
        :return:
        """
        if self.state is STATE_READY: return True
        if self.state is STATE_RAW:
            self.hashid = self.packos.hash(self.path)
            rmflag = False
            if self.mkpm.hash.get(self.mname):
                if self.hashid == self.mkpm.hash[self.mname]:
                    self.state = STATE_RSTRUCT
                    self.instantiate()
                    return
                else:
                    rmflag = True

            try:
                _dir = self.packos.getdir(self.path)
                new_path = self.packos.join(self.mkpm.mkppath, _dir)
                if rmflag:
                    self.packos.remove(new_path)
                self.packos.copy(self.path, new_path)
                self.path = new_path  # 路径变化
                self.state = STATE_RBUF
            except Exception as err:
                print(f"{self}:\n\tException in STATE{self.state.__class__.__name__}: {err}")
        else:
            print(f"{self} unable to load to buffer, due to it's unsuitable state: " + self.state.__name__)

    def restruct(self):
        """
        对位于[buffer]下的此mod进行代码重构, 目前这一步非常脆弱, 请尽量规范编写mod的import部分以规避bug
        该操作只能在state为STATE_RBUF时进行
        :return:
        """
        if self.state is STATE_READY: return True
        if self.state is STATE_RBUF:
            PyRestruct(self.path, self.mkpm.MKBUFNAME + '.')
            self.state = STATE_RSTRUCT
        else:
            print(f"{self} unable to restruct, due to it's unsuitable state: " + self.state.__name__)

    def instantiate(self):
        """
        最终加载, 本质上是从[buffer]中执行python的import操作
        :return:
        """
        if self.state is STATE_READY: return True
        if self.state is STATE_RSTRUCT:
            self.mkpm.hash[self.mname] = self.hashid
            self.mkpm.save(self.mkpm.MKHASHNAME)
            # print(self.pypath)
            self.code = importlib.import_module(self.pypath)
            self.state = STATE_READY
        else:
            print(f"{self} unable to load to instantiate, due to it's unsuitable state: " + self.state.__name__)

    def __str__(self):
        try:
            dirname = self.packos.getdir(self.path)
        except:
            dirname = "*[unknown]"
        txt = f"plugin:{dirname} - {self.state.__name__}"
        return txt


class MKPluginManager():
    MKBUFNAME = 'mktemp'
    MKHASHNAME = 'mkphash'
    MKINFONAME = 'mkpinfo'
    def __init__(self, target_abspath:str):
        self.path = target_abspath
        assert os.path.isdir(self.path), "expected dir, but got " + target_abspath
        self.packos = PackOS(self.path)
        self.mkppath = os.path.abspath(self.packos.sureDir(self.MKBUFNAME))
        self.files = Files(self.mkppath, '.pkl')
        self._start = False


        self.Loading()

    def Loading(self):
        self.hash    = self.files.get(self.MKHASHNAME)
        self.hash    = self.hash if self.hash else {}
        self.info    = self.files.get(self.MKINFONAME)
        self.info    = self.info if self.info else {}

        self.plugs = {}

        for name, info in self.info.items():
            self.add(info.path)

    def save(self, part=None):
        if part:
            if part == self.MKHASHNAME:
                self.files.set(self.MKHASHNAME, self.hash)
            elif part == self.MKINFONAME:
                self.files.set(self.MKINFONAME, self.info)
        else:
            self.files.set(self.MKHASHNAME, self.hash)
            self.files.set(self.MKINFONAME, self.info)

    def clear(self):
        self.hash = {}
        self.info = {}
        self.plugs = {}
        self.save()

    def clearInfo(self):
        self.info = {}
        self.plugs = {}
        self.save()

    def load(self, mkplug:MKPlug, state=STATE_READY):
        if state == STATE_RAW: return True
        if mkplug.raw: mkplug.load2buf()
        if state == STATE_RBUF: return True
        if mkplug.rbuf: mkplug.restruct()
        if state == STATE_RSTRUCT: return True
        if mkplug.rstruct: mkplug.instantiate()
        if state == STATE_READY: return True
        return False

    def add(self, path:str):
        plugin = MKPlug(self, path)
        self.plugs[plugin.mname] = plugin
        self.info[plugin.mname] = plugin.info
        self.save(self.MKINFONAME)

        if self._start:
            self.load(plugin)

    def list(self):
        return list(self.info.keys())

    def remove(self, name:str):
        if self.info.get(name):
            return True
        self.info.pop(name)
        self.plugs.pop(name)
        self.save(self.MKINFONAME)
        if self._start:
            ...

    def start(self):
        for k, plug in self.plugs.items():
            self.load(plug)

    def get(self, plug_name:str) -> MKPlug:
        return self.plugs.get(plug_name)

    def __getitem__(self, item):
        return self.plugs.get(item)
