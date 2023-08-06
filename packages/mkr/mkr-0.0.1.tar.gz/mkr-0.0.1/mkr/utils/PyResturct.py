# -*- coding: utf-8 -*-
import re
import os
import sys  # 打印python解释器位置
import importlib as imp
from mkr.utils.PackOS import BiasPath

class PyFile:
    def __init__(self, root:str, file_path:str):
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
                    raise Exception(f"no union: root: {root}, path: {path}")

    def read(self):
        return open(self._raw_fpath, 'r').read()

    def write(self, txt:str):
        return open(self._raw_fpath, 'w').write(txt)

    def restruct(self, new_rel:str):
        nr = new_rel
        pn = os.path.basename(self.root)

        # 有两种库情况
        # 一种是库内导入，这种导入内的导入至少有一个文件不包含{pn}
        # 另一种是库外导入，这种导入内的导入所有导入均以{pn}开头

    def __str__(self):
        rels = "-"
        for rel in self.rel:
            rels += f"{rel}."
        rels = rels[:-1]
        txt = f"PyFile: {self.fname}{rels}"
        return txt


def IsGlobalModule(module:str):
    try:
        spec = imp.util.find_spec(module)
    except ModuleNotFoundError:
        spec = None
    # 'cached', 'has_location', 'loader', 'loader_state', 'name', 'origin', 'parent', 'submodule_search_locations'
    # if spec: print(sys.executable, spec.origin)
    return spec

def ExtraModules(line):
    # 提取所有导入模块名称
    _rs = re.sub('\s', '', line)
    if _rs[:4] == 'from':
        ir = re.findall('from\s+[\w\.]+\s+import', line)
        assert len(ir) == 1, "unknown case: '" + str(line) + "'"
        ir = ir[0]
        modules = [re.sub('\s', '', ir[4:-6])]
    else:
        ir = re.findall('import.+', line)
        assert len(ir) == 1, "unknown case: '" + str(line) + "'"
        ir = ir[0]
        # 整理导入模块
        irs = []
        for _ir in ir[6:].split(','):
            __ir = re.sub('\s', '', _ir)
            if __ir:
                irs += [_ir]
        # 提取module
        modules = []
        for ir in irs:
            ir = re.sub('\sas\s', '{as}', ir)
            index_as = ir.find("{as}")
            if index_as != -1:
                ir = ir[:index_as]
            _ir = re.sub('\s', '', ir)
            if _ir:
                modules += [_ir]
    return modules

def PyRestruct(root_path:str, pre:str):
    """
    python代码(关于import路径)重构
    :param root_path: abs path. 目标mod根目录
    :param pre: 'xxx.'
    :return:
    """
    assert os.path.isabs(root_path), "root_path must be a abspath. not " + root_path
    assert os.path.isdir(root_path), "root_path must be a dirpath. not " + root_path
    mod_name = os.path.basename(root_path)
    pre = pre + mod_name + "."
    # find py files:
    pyfiles = []  # PyFile
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file[-3:].lower() == '.py':
                path = os.path.join(root, file)
                pyfiles += [PyFile(root_path, path)]

    pn = os.path.basename(root_path)
    nopn_flag = False

    # 先试探一波，分析出这是一个项目还是一个包
    import_partern = '\n.*f?r?o?m?.*import.+\n'
    prs = {}
    for i in range(len(pyfiles)):
        pf = pyfiles[i]
        prs[i] = '\n' + pf.read().replace('\n', '\n\n') + '\n'
    for txt in prs.values():
        # 提取所有import情形
        results = [result[1:-1] for result in re.findall(import_partern, txt)]
        # print(results)

        for result in results:
            modules = ExtraModules(result)

            # 至此，已经从此文件中提取到了所有导入module的名称
            # 现在检查这些module是否存在全局不可见且又没有以{pn}开头的模块
            for module in modules:
                visiable = IsGlobalModule(module)
                if not visiable:
                    # 检查是否以{pn}.开头
                    tm = module + ' '
                    if tm.find('.') != -1:
                        if module[:len(pn) + 1] != (pn + '.'):
                            nopn_flag = True
                            break
                    elif module[:len(pn)] != pn:
                        nopn_flag = True
                        break

            # 检查是否已有flag结果
            if nopn_flag:
                break


    # 试探结束，根据试探的分析进行重构
    def sub_fn(matched):
        txt = matched.group()
        # txt = txt[1:-1]
        # # 整理一下
        # def _remove_s(m):
        #     _str    = m.string
        #     _span   = m.span()
        #     _left   = re.sub('\s', '', _str[:_span[0]])
        #     _right  = re.sub('\s', '', _str[_span[1]:])
        #
        #     if _left == 'import' or _left == 'from': return _str
        #     elif _right[:6] == 'import': return _str
        #     else: return ''
        # txt = re.sub('\s', ' ', txt)
        modules = ExtraModules(txt)

        news = []
        # 重排序，长的在前
        for m in modules:
            flag = False
            for i in range(len(news)):
                n = news[i]
                if len(m) > len(n):
                    news.insert(i, m)
                    flag = True
                    break
            if not flag:
                news += [m]
        modules = news

        rep = {}
        # 重构的核心代码
        for i in range(len(modules)):
            module = modules[i]
            index = txt.find(module)
            # print(module, txt)
            assert index != -1, "Cannot mix \\s to module name. Line: '" + txt + "'"
            if not IsGlobalModule(module):
                key, value = f'k_{i}', pre + module
                txt = txt[:index] + "{" + key + "}" + txt[index + len(module):]
                rep[key] = value
        # print("rep: ", rep)
        return txt.format(**rep)



    # 完成重构
    for i, v in prs.items():
        v = re.sub(import_partern, sub_fn, v)
        v = v[1:-1].replace('\n\n', '\n')
        pyfiles[i].write(v)

    return True
        # print(v)
        # print("-" * 20)
# 'end', 'endpos', 'expand', 'group', 'groupdict', 'groups', 'lastgroup', 'lastindex', 'pos', 're', 'regs', 'span', 'start', 'string'

if __name__ == '__main__':
    PyRestruct(r'C:\Users\Administrator\Desktop\test', 'mktemp.')
