# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import json
import configparser
import numpy as np
import os
import torch
import random
import struct
import cv2
from JoTools.txkjRes.deteRes import DeteRes
from JoTools.txkjRes.deteObj import DeteObj
from torch.backends import cudnn
from .abstractBase import detection


class FasterDetectionPytorch(detection):

    def __init__(self, section, cfg_path, gpu_id, model_path=None):
        super(FasterDetectionPytorch, self).__init__(section, cfg_path)
        self.gpu_id = gpu_id
        self.model_path = model_path
        self.classes = tuple(self.classes.strip(',').split(','))
        self.visible_classes = tuple(self.visible_classes.strip(',').split(','))
        self.conf_threshold = float(self.conf_threshold)
        self.device = self.select_device(self.gpu_id)

    def model_restore(self):
        try:
            self.model = torch.load(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            self.warmUp()
            print("* load faster model success : {0}".format(self.section))
        except Exception as e:
            print(e)
            raise ValueError("* load faster model failed : {0}".format(self.section))

    def warmUp(self):
        im = 128 * np.ones((1000, 1000, 3), dtype=np.uint8)
        self.detect(im)

    @torch.no_grad()
    def detect(self, im, resize_ratio=1, image_name="test.jpg"):
        # im 进行 resize，
        im_height, im_width = im.shape[:2]
        im = cv2.resize(im, (int(im_width*resize_ratio), int(im_height*resize_ratio)))
        img_tensor = torch.from_numpy(im / 255.).permute(2, 0, 1).float().cuda()
        out = self.model([img_tensor])
        res = []
        # 结果处理并输出
        boxes, labels, scores = out[0]['boxes'], out[0]['labels'], out[0]['scores']
        # 清空缓存
        torch.cuda.empty_cache()
        #
        index = 0
        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes[i]
            score = scores[i].item()
            if score > self.conf_threshold:
                index += 1
                obj = self.classes[labels[i].item() - 1]
                if obj in self.visible_classes:
                    # 将 resize 后的数据映射回来
                    res.append([obj, index, int(x1/resize_ratio), int(y1/resize_ratio), int(x2/resize_ratio), int(y2/resize_ratio), str(score)])
        return res

    def detectSOUT(self, path=None, image=None, image_name="default.jpg"):
        dete_res = DeteRes()
        dete_res.img_path = path
        dete_res.file_name = image_name
        if not isinstance(image, np.ndarray):
            image = dete_res.get_img_array()
        bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = self.detect(bgr, image_name=image_name)
        # get deteRes
        assign_id = 0
        for each_obj in results:
            # x1, y1, x2, y2, tag, conf
            dete_res.add_obj(each_obj[2], each_obj[3], each_obj[4], each_obj[5], tag=each_obj[0], conf=float(each_obj[6]), assign_id=assign_id)
            assign_id += 1
        return dete_res
