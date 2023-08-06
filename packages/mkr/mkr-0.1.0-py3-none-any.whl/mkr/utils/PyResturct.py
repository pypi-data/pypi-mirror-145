# -*- coding: utf-8 -*-
import re
import os
import sys  # 打印python解释器位置
from importlib.util import find_spec
from mkr.utils.PackOS import BiasPath


class PyFile:
    def __init__(self, root: str, file_path: str):
        # 安全性检查
        bp = BiasPath(root, "")
        dp = BiasPath(file_path, "")
        assert bp.isdir(), "target path must be a dir, not : " + str(bp)
        assert bp.isabs(), "target path must be a abspath, not : " + str(bp)
        assert dp.isfile(), "target path must be a file, not : " + str(dp)
        assert dp.isabs(), "target path must be a abspath, not : " + str(dp)
        assert str(dp)[-3:].lower() == '.py', "target path must be a pyfile, not : " + str(dp)

        # 初始化
        self.root = root
        self.rel = []
        self.fname = os.path.basename(file_path)[:-3]
        self._raw_fpath = file_path

        path = os.path.dirname(file_path)
        if root != path:
            while 1:
                _dir, _name = os.path.dirname(path), os.path.basename(path)
                self.rel.insert(0, _name)
                if _dir and _name:
                    if _dir == root:
                        break
                else:
                    raise Exception(f"no path union: root: {root}, path: {path}")

    def read(self):
        return open(self._raw_fpath, 'r').read()

    def write(self, txt: str):
        return open(self._raw_fpath, 'w').write(txt)

    def __str__(self):
        rels = "-"
        for rel in self.rel:
            rels += f"{rel}."
        rels = rels[:-1]
        txt = f"PyFile: {self.fname}{rels}"
        return txt


class ImportSegment:
    ORDa = ord('a')
    ORDz = ord('z')
    ORDA = ord('A')
    ORDZ = ord('Z')

    def __init__(self, segment: str, preix: str):
        self.seg = segment
        self.pre = preix

    @staticmethod
    def replace(match, preix):
        seg = match.group()[:-1]  # 去掉\n
        # print('seg: ', seg)
        imp_seg = ImportSegment(seg, preix)
        return imp_seg.solution()

    @property
    def prestr(self):
        if hasattr(self, '_prestr'): return self._prestr
        ret, i = '', 0
        while 1:
            if 127 == ord(self.seg[i]) <= 31: break
            ret += self.seg[i]
            i += 1
        self._prestr = ret
        return ret

    @property
    def isfrom(self):
        if hasattr(self, '_isfrom'): return self._isfrom
        index = self.seg.find('from')
        if index != -1:  # 仍有可能为 import fromlib这样的可能
            for i in range(0, index):
                if self.ORDA < ord(self.seg[i]) < self.ORDz:
                    self._isfrom = False
                    return
            self._isfrom = True
        else:
            self._isfrom = False
        return self._isfrom

    @property
    def afterimport(self):
        if hasattr(self, '_afterimport'): return self._afterimport
        if self.isfrom:
            self._afterimport = None  # from xxx import 后面的东西已经不重要了
        else:
            self._afterimport = self.seg[self.importpos + 6:] if self.importpos else None
        return self._afterimport

    @property
    def importpos(self):
        if hasattr(self, '_importpos'): return self._importpos
        if self.isfrom:
            match = re.search('\simport\s', self.seg)
            self._importpos = match.span()[0] if match else None
        else:
            index = self.seg.find('import')
            self._importpos = index if index != -1 else None
        return self._importpos

    @property
    def frompos(self):
        if hasattr(self, '_frompos'): return self._frompos
        index = self.seg.find('from')
        self._frompos = index if self.isfrom and index != -1 else None
        return self._frompos

    def newName(self, module: str, pre: str) -> str:
        """
        获取一个module的新名称
        :param module: 模块名称
        :param pre: 模块新前缀(不能有空白字符)
        :return: str
        """
        try:
            __import__(module)
            return module
        except ImportError:
            pre = pre if pre[-1] == '.' else pre + '.'
            return pre + module

    def solution(self):
        """
        为这个导入片段制定解决方案
        执行解决方案时需要暂时在sys.path中移除当前目录
        :param preix: 新的前缀
        :return:
        """
        if self.isfrom:  # from 模式
            module = re.sub('\s', '', self.seg[self.frompos + 4: self.importpos])
            return f"{self.seg[:self.frompos + 4]} {self.newName(module, self.pre)} {self.seg[self.importpos:]}\n"
        else:  # import 模式
            left, right = self.seg[:self.importpos + 6], ''
            for piece in self.seg[self.importpos + 6:].split(','):
                if not piece: continue
                match  = re.search('\sas\s', piece)
                index  = match.span()[0] if match else len(piece) + 1
                module = re.sub('\s', '', piece[:index])
                _new_  = self.newName(module, self.pre)
                right += f"{_new_} {piece[index:]}, "
                # import 本地库 没有as是非常危险的
                if _new_ != module and match is None:
                    print(f"Warning: Dangerous import: '{self.seg}'. Using 'from xxx import ...' or 'import xxx as ...' is a better choice.")

            if right: right = right[:-2]
            return f"{left} {right}\n"


def PyRestruct(root_path: str, pre: str):
    """
    python代码(关于import路径)重构
    :param root_path: abs path. 目标mod根目录
    :param pre: 'xxx.'
    :return:
    """
    # 先获取所有文件
    assert os.path.isabs(root_path), "root_path must be a abspath. not " + root_path
    assert os.path.isdir(root_path), "root_path must be a dirpath. not " + root_path

    # find py files:
    pyfiles = []  # PyFile
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file[-3:].lower() == '.py':
                path = os.path.join(root, file)
                pyfiles += [PyFile(root_path, path)]

    pre = pre if pre[-1] == '.' else pre + '.'
    pre = pre + os.path.basename(root_path) + "."

    # 开始输出
    sys.path.remove(os.getcwd())
    import_partern = '[^\n\s:]*f?r?o?m?[\s\w]*import.+\n'
    for py in pyfiles:
        changed = re.sub(import_partern, lambda match: ImportSegment.replace(match, pre), py.read())
        # print(changed)
        py.write(changed)
    sys.path.append(os.getcwd())


if __name__ == '__main__':
    PyRestruct(r'C:\Users\Administrator\Desktop\test', 'mktemp')
