# -*- coding: utf-8 -*-
import os
from shutil import copytree, rmtree
"""
package文件管理
"""

import hashlib


def cal_file_md5(filt_path, hasher=None):
    root = not bool(hasher)

    if hasher is None:
        hasher = hashlib.md5()

    with open(filt_path, "rb") as f:
        while 1:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)

    if root: return hasher.hexdigest()
    return hasher


def cal_dir_md5(folder, hasher=None):
    if not os.path.exists(folder):
        print("Folder doesn't exist %s" % folder)
        return

    root = not bool(hasher)

    if hasher is None:
        hasher = hashlib.md5()

    items = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            items += [cal_dir_md5(path, hasher)]
        else:
            items += [cal_file_md5(path, hasher)]

    if root: return hasher.hexdigest()
    return hasher



class BiasPath:
    def __init__(self, raw_path:str, rel_path:str):
        self._path = os.path.join(raw_path, rel_path) if rel_path else raw_path
        self._exist = os.path.exists(self._path)
        self._file = True if self._exist and os.path.isfile(self._path) else False
        self._dir = True if self._exist and os.path.isdir(self._path) else False

    def __str__(self):
        return self._path

    def isabs(self):
        return os.path.isabs(self._path)

    def isrel(self):
        return not os.path.isabs(self._path)

    def isfile(self):
        return self._exist and self._file

    def isdir(self):
        return self._exist and self._dir

    def isexist(self):
        return self._exist



class PackOS:
    def __init__(self, ppath:str=None):
        if os.path.isabs(ppath):
            ppath = os.path.abspath(ppath)
        assert os.path.isdir(ppath), "project path must be a folder. but file path get: " + ppath
        self.path = ppath

    def bias(self, relpath:str):
        if os.path.isabs(relpath):
            return BiasPath(relpath, "")
        else:
            return BiasPath(self.path, relpath)

    def sureDir(self, path:str):
        """
        确保某个目录存在, 如果目标目录不存在, 会试图进行创建
        :param path:
        :return:
        """
        bp = self.bias(path)
        if bp.isdir():
            return path

        os.makedirs(path)
        return path

    def copy(self, source_path:str, dest_path:str, isdir:bool=False, isfile:bool=False, empty:bool=False):
        """
        拷贝a到b, a和b既可以是文件也可以是folder(但需要指定参数)
        路径既可以是绝对路径也可以是相对路径(相对初始化传入的ppath)
        :param source_path:
        :param dest_path:
        :param isdir:
        :param isfile:
        :param empty:
        :return:
        """
        bp = self.bias(source_path)
        dp = self.bias(dest_path)
        assert bp.isexist(), "source is empty. source " + str(bp)
        if isdir:
            assert bp.isdir(), "from path must be a dir, not : " + str(bp)
            assert dp.isdir(), "to path must be a dir, not : " + str(dp)
        if isfile:
            assert bp.isfile(), "from path must be a file, not : " + str(bp)
            assert dp.isfile(), "to path must be a file, not : " + str(dp)
        if empty:
            assert not dp.isexist(), "mod to path must be a dir, not file: " + str(dp)
        if dp.isexist():
            rmtree(str(dp))

        copytree(str(bp), str(dp))
        return True

    def remove(self, path:str):
        bp = self.bias(path)
        if bp.isdir():
            rmtree(str(bp))
            return True
        elif bp.isfile():
            os.remove(str(bp))
            return True
        return False

    def getdir(self, path:str):
        bp = self.bias(path)
        assert bp.isdir(), "target path must be a dir, not : " + str(bp)
        return os.path.basename(path)

    def join(self, *args):
        return os.path.join(*args)

    def hash(self, path:str):
        bp = self.bias(path)
        assert bp.isexist(), "file or dir doesn't exist: " + str(bp)
        if bp.isdir():
            return cal_dir_md5(str(bp))
        return cal_file_md5(str(bp))