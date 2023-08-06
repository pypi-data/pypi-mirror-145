# -*- coding: utf-8  -*-
# -*- author: zhangyi -*-

import os
import cv2
import configparser
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from .viT_libs.vit_model import vit_base_patch16_224_in21k as create_model
from .abstractBase import detection


class ClsViTDetection(detection):

    def __init__(self, section, cfg_path, gpu_id, model_path=None):
        super(ClsViTDetection, self).__init__(section, cfg_path)
        self.section = section
        self.gpu_id = gpu_id
        self.model_path = model_path
        self.classes = tuple(self.classes.strip(',').split(','))
        cuda_info = "cuda:"+str(self.gpu_id)
        self.device = torch.device(cuda_info)
        self.norm_size = int(self.norm_size)
        #
        self.data_transform = transforms.Compose(
            [transforms.Resize(self.norm_size),
             transforms.CenterCrop(224),
             transforms.ToTensor(),
             transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

    def model_restore(self):
        try:
            torch.cuda.empty_cache()
            self.model = create_model(num_classes=int(self.num_classes), has_logits=False).to(self.device)
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model.eval()
            self.warmUp()
            print("* load Vit model success : {0}".format(self.section))
        except Exception as e:
            print(e)
            raise ValueError("* load Vit model failed : {0}".format(self.section))

    def warmUp(self):
        im = 128 * np.ones((self.norm_size, self.norm_size, 3), dtype=np.uint8)
        self.detect(im)

    @torch.no_grad()
    def detect(self, im):
        image = Image.fromarray(im.astype('uint8')).convert('RGB')  # np.array==>Image
        img = self.data_transform(image)
        img = torch.unsqueeze(img, dim=0)
        output = torch.squeeze(self.model(img.to(self.device))).cpu()
        proba= max(torch.softmax(output, dim=0).numpy())  # 概率
        label = torch.argmax(torch.softmax(output, dim=0)).numpy()  # 输出为: 0 or 1 or 2
        label = self.classes[label]
        return label, proba


