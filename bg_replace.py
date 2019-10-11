# -*- coding: utf-8 -*- 
# @Time     : 2019-10-11 15:26
# @Author   : binger
import numpy as np


def pil_to_array(pilImage):
    import numpy as np
    """Load a `PIL image`_ and return it as a numpy array.

    .. _PIL image: https://pillow.readthedocs.io/en/latest/reference/Image.html

    Returns
    -------
    numpy.array

        The array shape depends on the image type:

        - (M, N) for grayscale images.
        - (M, N, 3) for RGB images.
        - (M, N, 4) for RGBA images.

    """
    if pilImage.mode in ['RGBA', 'RGBX', 'RGB', 'L']:
        # return MxNx4 RGBA, MxNx3 RBA, or MxN luminance array
        return np.asarray(pilImage)
    elif pilImage.mode.startswith('I;16'):
        # return MxN luminance array of uint16
        raw = pilImage.tobytes('raw', pilImage.mode)
        if pilImage.mode.endswith('B'):
            x = np.frombuffer(raw, '>u2')
        else:
            x = np.frombuffer(raw, '<u2')
        return x.reshape(pilImage.size[::-1]).astype('=u2')
    else:  # try to convert to an rgba image
        try:
            pilImage = pilImage.convert('RGBA')
        except ValueError:
            raise RuntimeError('Unknown image mode')
        return np.asarray(pilImage)  # return MxNx4 RGBA array


def bg_replace_by_cv2(im_or_path, replaced_color=None):
    if not isinstance(im_or_path, np.ndarray):
        np_image = cv2.imread(im_or_path, -1)
    else:
        np_image = im_or_path
    replaced_color = replaced_color or (255, 255, 255, 255)
    dst_color = (0, 0, 0, 0)

    W, H, A = np_image.shape
    for h in range(H):
        for w in range(W):
            color_cur = np_image[w, h]
            if (color_cur == replaced_color).all():
                np_image[w, h] = dst_color
    return np_image


def bg_replace_by_pil(image_or_path, replaced_color=None):
    from PIL import ImageFile
    if not isinstance(image_or_path, ImageFile.ImageFile):
        image = Image.open(path)
    else:
        image = image_or_path

    image = image.convert('RGBA')
    w, h = image.size

    replaced_color = replaced_color or (255, 255, 255, 255)
    dst_color = (0, 0, 0, 0)
    for i in range(h):
        for j in range(w):
            dot = (j, i)
            color_cur = image.getpixel(dot)
            if color_cur == replaced_color:
                image.putpixel(dot, dst_color)
    return image


def bg_replace_by_matplotlib(im_or_path, replaced_color=None):
    from matplotlib import image as mg
    if not isinstance(im_or_path, np.ndarray):
        np_image = mg.imread(im_or_path)
    else:
        np_image = im_or_path

    # replaced_color = replaced_color or (1, 1, 1, 1)
    dst_color = (0, 0, 0, 0)

    w, h, alpha = np_image.shape
    for i in range(w):
        for j in range(h):
            aa = sum(np_image[i, j])
            if aa == 4:
                np_image[i, j] = dst_color
    return np_image


if __name__ == "__main__":
    from PIL import PngImagePlugin, ImageFile
    from PIL import Image
    import cv2

    path = '/Users/yangshujun/self/handle_css/1.png'
    # image = Image.open(path)
    # print(isinstance(image, ImageFile.ImageFile))
    # bg_replace_by_pil(image_or_path=path)
    # bg_replace_by_cv2(path)
    bg_replace_by_matplotlib(path)
