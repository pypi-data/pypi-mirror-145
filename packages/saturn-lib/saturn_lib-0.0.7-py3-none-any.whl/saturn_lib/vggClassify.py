# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import cv2
import torch
import configparser
import numpy as np
import uuid
from .abstractBase import detection


class VggClassify(detection):

    def __init__(self, section, cfg_path, gpu_id, model_path=None):
        super(VggClassify, self).__init__(section=section, cfg_path=cfg_path)
        self.section = section
        self.gpu_id = gpu_id
        self.model_path = model_path
        self.classes = tuple(self.classes.strip(',').split(','))
        self.device = self.select_device(self.gpu_id)

    def model_restore(self):
        """加载模型"""
        try:
            if not self.model_path:
                raise ValueError("model path is None")
            self.model = torch.load(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            self.warmUp()
            print("* load vgg model success : {0}".format(self.section))
        except Exception as e:
            print(e)
            raise ValueError("* load vgg model failed : {0}".format(self.section))

    def warmUp(self):
        im = 123 * np.ones((224, 224, 3), dtype=np.uint8)
        self.detect(im)

    @torch.no_grad()
    def detect(self, im, image_name='test.jpg'):
        """进行检测"""
        if im is None:
            return None, 0
        else:
            src_img = cv2.resize(im, (224, 224))
            img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
            img_tensor = torch.from_numpy(img / 255.).permute(2, 0, 1).float().cuda()
            img_tensor = torch.unsqueeze(img_tensor, 0)
            out = self.model(img_tensor)

            if hasattr(out, "data"):
                # softmax
                out = torch.nn.functional.softmax(out, 1)
                proba, pred = out.data.max(1, keepdim=True)
                pre = pred.data.item()
                proba = proba.data.item()

                # 清空缓存
                torch.cuda.empty_cache()
                return self.classes[int(pre)], proba
            else:
                return None, 0












