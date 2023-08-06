#! /usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(__file__))

import cv2
import torch
import configparser
import numpy as np
from .abstractBase import detection
from .yolov5_libs.models.experimental import attempt_load
from .yolov5_libs.datasets import letterbox
from .yolov5_libs.torch_utils import select_device
from .yolov5_libs.general import check_img_size, non_max_suppression, scale_coords
from JoTools.txkjRes.deteRes import DeteRes
from JoTools.txkjRes.deteObj import DeteObj
#from JoTools.utils.DecoratorUtil import DecoratorUtil



class YOLOV5Detection(detection):

    def __init__(self, section, cfg_path, gpu_id, model_path=None):
        super(YOLOV5Detection, self).__init__(section, cfg_path)
        self.gpu_id = gpu_id
        self.model_path = model_path
        self.device = select_device(str(self.gpu_id))
        self.classes = tuple(self.classes.strip(',').split(','))
        self.visible_classes = tuple(self.visible_classes.strip(',').split(','))
        self.class_dict = dict(zip(range(len(self.classes)), self.classes))
        
    def model_restore(self):
        try:
            self.model = attempt_load(self.model_path, map_location=self.device)
            self.stride = int(self.model.stride.max())
            self.imgsz = check_img_size(int(self.img_size), s=self.stride)
            self.model.half().eval()
            self.warmUp()
            print("* load yolov5 model success : {0}".format(self.section))
        except Exception as e:
            print(e)
            raise ValueError("* load yolov5 model failed : {0}".format(self.section))

    def warmUp(self):
        self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))

    def detect(self, image, image_name="default.jpg"):
        # difference between test.py(better results) and detect.py
        h0, w0 = image.shape[:2]  # orig hw
        r = self.imgsz / max(h0, w0)  # resize image to img_size
        if r != 1:  # always resize down, only resize up if training with augmentation
            interp = cv2.INTER_AREA if r < 1 and not self.augment else cv2.INTER_LINEAR
            img = cv2.resize(image, (int(w0 * r), int(h0 * r)), interpolation=interp)
        else:
            img = image

        img = letterbox(img, self.imgsz, stride=self.stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img).astype(np.float32)
        img = torch.from_numpy(img).to(self.device).half()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        with torch.no_grad():
            pred = self.model(img, augment=self.augment)[0]
            det = non_max_suppression(pred, float(self.conf_threshold), float(self.iou_threshold), multi_label=True,
                                      classes=[self.classes.index(c) for c in self.visible_classes])[0]

        if len(det):
            boxes = scale_coords(img.shape[2:], det[:, :4], image.shape).round().cpu().numpy()
            scores = det[:, -2].cpu().numpy()
            classes = (det[:, -1].cpu().numpy().astype(np.int8))
            # torch.cuda.empty_cache()
            return boxes, classes, scores
        else:
            return [], [], []

    def post_process(self, boxes, classes, scores):
        objects = []
        for i in range(len(boxes)):
            xmin, ymin, xmax, ymax = boxes[i]
            label = self.class_dict[classes[i]]
            objects.append([label, i, int(xmin), int(ymin), int(xmax), int(ymax), float(scores[i])])
        return objects

    #@DecoratorUtil.time_this
    def detectSOUT(self, path=None,image=None, image_name="default.jpg",output_type='txkj'):
        dete_res = DeteRes()
        dete_res.img_path = path
        dete_res.file_name = image_name
        if image is None:
            image = dete_res.get_img_array()
        bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        boxes, classes, scores = self.detect(bgr,image_name)
        for i in range(len(boxes)):
            xmin, ymin, xmax, ymax = boxes[i]
            label = self.class_dict[classes[i]]
            prob = float(scores[i])
            dete_obj = DeteObj(x1=int(xmin), y1=int(ymin), x2=int(xmax), y2=int(ymax), tag=label, conf=prob, assign_id=i)
            dete_res.add_obj_2(dete_obj)
        if output_type == 'txkj':
            return dete_res
        elif output_type == 'json':
            pass
        return dete_res

