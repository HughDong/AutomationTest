# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
from base.app_ui.android.demoProject.app_ui_android_demoProject_read_config import APP_UI_Android_DemoProject_Read_Config
from appium import webdriver
from base.read_app_ui_config import Read_APP_UI_Config
from common.appium.appOperator import AppOperator
from common.fileTool import FileTool
from init.app_ui.android.demoProject.demoProjectInit import DemoProjectInit
import os

class APP_UI_Android_demoProject_Client(object):

    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self,is_need_reset_app=False):
        if self.__inited is None:

            self.config = Read_APP_UI_Config().app_ui_config
            self.device_info=FileTool.readJsonFromFile('config/app_ui_tmp/'+str(os.getppid()))
            self.demoProject_config = APP_UI_Android_DemoProject_Read_Config('config/demoProject/%s'%self.device_info['app_ui_config']).config
            self.current_desired_capabilities = FileTool.readJsonFromFile('config/app_ui_tmp/' + str(os.getppid()) + '_current_desired_capabilities')
            self._appium_hub='http://'+self.device_info['server_ip']+':%s/wd/hub'%self.device_info['server_port']
            self._init(self.demoProject_config.init)
            self.driver = webdriver.Remote(self._appium_hub,desired_capabilities=self.current_desired_capabilities)
            self.appOperator = AppOperator(self.driver,self._appium_hub)

            self.__inited=True
        if is_need_reset_app:
            self.appOperator.reset_app()

    def _init(self,is_init=False):
        print('初始化android基础数据......')
        DemoProjectInit().init(is_init)
        print('初始化android基础数据完成......')
