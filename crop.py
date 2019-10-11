# -*- coding: utf-8 -*- 
# @Time     : 2019-10-11 17:39
# @Author   : binger

import cv2
from PIL import Image
import numpy as np

# cv2.THRESH_BINARY_INV 二制化，只有0（黑）和255（白），默认白色有用
BINARY_WHITE = 255
BINARY_BLACK = 0
BINARY_USE_INV = BINARY_WHITE


def crop_edge_area(image, color_range=None, alpha_range=None, is_run_crop=True):
    """
    对于rgba图像获取 alpha 的非零区域
    对于rgb图像，获取非零或者255的区域
    :param image: PIL.ImageFile.ImageFile
    :param color_range: 剪切边界的颜色区域
    :param alpha_range: 剪切边界透明区域
    :param is_run_crop: 是否扣除区域
    :return:
    """

    from PIL import ImageFile
    assert isinstance(image, ImageFile.ImageFile)

    color_range = color_range or (200, 255)
    if image.mode == "P":
        image = image.convert("RGBA")
    crop_image = np.asarray(image)

    if len(crop_image.shape) == 2:
        # 灰度图
        ret, gray_image = cv2.threshold(crop_image, color_range[0], color_range[1], cv2.THRESH_BINARY_INV)
        points = np.argwhere(gray_image[:, :] == BINARY_WHITE)[:, ::-1]
        if points.size > 0:
            if is_run_crop:
                x, y, w, h = cv2.boundingRect(points)
                roi = crop_image[y:y + h, x:x + w]
                roi = Image.fromarray(roi)
                return True, roi
            else:
                return True, image
        else:
            return False, image

    elif crop_image.shape[2] == 3:
        # RGB 模式的图形
        gray_image = cv2.cvtColor(crop_image, cv2.COLOR_RGB2GRAY)
        ret, gray_image = cv2.threshold(gray_image, color_range[0], color_range[1], cv2.THRESH_BINARY_INV)
        points = np.argwhere(gray_image[:, :] == BINARY_WHITE)[:, ::-1]
        if points.size > 0:
            if is_run_crop:
                x, y, w, h = cv2.boundingRect(points)
                roi = crop_image[y:y + h, x:x + w]
                roi = Image.fromarray(roi)
                return True, roi
            else:
                return True, image
        else:
            return False, image
    elif crop_image.shape[2] == 4:
        # RGBA 模式 可能存在透明
        alpha_range = alpha_range or (255 * 0.05, 255)

        split_image = cv2.split(crop_image)
        points = np.argwhere((split_image[3] > alpha_range[0]) & (split_image[3] < alpha_range[1]))
        if points.size > 0:
            if is_run_crop:
                y, x, h, w = cv2.boundingRect(points)
                roi = crop_image[y:y + h, x:x + w]
                roi = Image.fromarray(roi)
                return True, roi
            else:
                return True, image
        else:
            return False, image


