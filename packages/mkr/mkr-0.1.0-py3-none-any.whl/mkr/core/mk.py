# -*- coding: utf-8 -*-
import os

from mkr.core.mkp import MKPluginManager


class MicroKernel:
    """
    微核架构 - 基于外部内核框架
    提供python插件管理(python插件做成独立python项目的形式，最后在其中加入__init__.py作为mod入口)
    NOTE: 你做的python插件在import时小心和mk项目中的文件重名，不然可能会出现循环导入
    通过.add方法返回插件对象, 成功启动微核后，可以通过插件对象.code访问到上述__init__.py的内容
    """
    def __init__(self, core_frame:object, plugin_path_name:str='plugins'):
        """

        :param core_frame: 微核系统的内核框架
        :param plugin_path_name: 插件目录的名称, 之后将所有mod放在该名称的路径下.
        """
        self.path = os.getcwd()
        self.core = core_frame
        self.mods = []
        self.plugin_path = os.path.abspath(plugin_path_name)

        # 添加组件
        self.mkpm = MKPluginManager(self.path)
        self.packos = self.mkpm.packos

        # 初始化mod目录
        self.packos.sureDir(self.plugin_path)
        self.mkpm.clearInfo()
        self.loadmods()


    def add(self, path:str):
        """
        添加mod, 返回插件对象
        :param path: mod路径
        :return:
        """
        mod = self.mkpm.add(path)
        if mod:
            self.mods += [mod]
        return mod

    def list(self):
        """
        查看当前已安装的mod
        :return: [names]
        """
        return self.mkpm.list()

    def remove(self, name:str):
        """
        移除指定名称的mod
        :param name:
        :return:
        """
        return self.mkpm.remove(name)

    def loadmods(self):
        """
        在plugin_path下加载mod
        该函数自动执行，不必由用户操作
        :return:
        """
        for fname in os.listdir(self.plugin_path):
            get = os.path.join(self.plugin_path, fname)
            if os.path.isdir(get):
                self.mods += [self.mkpm.add(get)]
        return self.mods

    def start(self):
        """
        启动微核架构
        :return:
        """
        self.mkpm.start()
        if self.core:
            if hasattr(self.core, 'start') and callable(self.core.start):
                self.core.start()
            else:
                print(f"Warning: inner core frame can not call 'start()'.")
        else:
            print(f"Warning: no inner core frame setted.")

    def __getitem__(self, item):
        plugin = self.mkpm.get(item)
        return None if plugin is None else plugin.code
