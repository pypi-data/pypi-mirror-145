# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import torch
import configparser


# todo 加密部分放在这边？还是使用其他方式进行加密？
# todo


class detection(object):

    def __init__(self, section, cfg_path):
        self.section = section
        self.config_path = cfg_path
        self.read_config_info()
        self.model = None
        self.device = torch.device('cuda')

    def read_config_info(self):
        """读取配置文件中当前模型对应的部分"""
        cf = configparser.ConfigParser()
        cf.read(self.config_path, encoding='utf-8')
        # assign section
        for each_option in cf.options(self.section):
            self.__dict__[each_option] = cf.get(self.section, each_option)
        # common section
        for each_option in cf.options("common"):
            self.__dict__[each_option] = cf.get("common", each_option)

    @staticmethod
    def select_device(device):
        cuda_info = "cuda:"+str(device)
        return torch.device(cuda_info)



if __name__ == "__main__":

    config_path = r"D:\Algo\txkj_lib\config.ini"
    a = detection("fzc_step_one", config_path)

    print("OK")
