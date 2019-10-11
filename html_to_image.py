# -*- coding: utf-8 -*- 
# @Time     : 2019-10-09 14:42
# @Author   : binger

from pyppeteer import launch
from contextlib import asynccontextmanager
import asyncio
from PIL import Image
from io import BytesIO

# 浏览器客户端句柄
browser = None


def asyncio_apply2(func):
    def wrap(*args, **kwargs):
        advocate_loop = asyncio.get_event_loop()
        return advocate_loop.run_until_complete(func(browser, *args, **kwargs))

    return wrap


async def init_browser():
    """
    初始化浏览器客户端
    :return: 浏览器句柄
    """
    global browser
    browser = await launch(autoClose=False)
    # autoClose: 脚本完成时自动关闭浏览器进程。默认为True。
    return browser


async def close():
    """
    关闭浏览器
    :return:
    """
    if browser:
        for _page in await browser.pages():
            _page.close()

        await browser.close()


@asynccontextmanager
async def create_page(browser):
    """
    创建浏览器上的页面（创建页面上下文）
    :param browser:
    :return:
    """
    page = await browser.newPage()
    yield page
    await page.close()


async def to_buffer(page, page_path, size, element_name=None):
    """
    https://hacpai.com/article/1566221786951
    截取浏览器客户端页面内容为buffer 格式（png）的数据
    :param page:
    :param page_path:
    :param size:
    :param element_name:
    :return:
    """
    await page.setViewport(viewport={"width": size[0], "height": size[1]})
    # await page.setJavaScriptEnabled(enabled=False)
    await page.goto(page_path)
    # await page.screenshot({'path': _OUTFILE, 'fullPage': True, 'omitBackground': "transparency"})
    if element_name:
        element = await page.querySelector(element_name)
        box = await element.boundingBox()
        # box = {'x': 15, 'y': 15, 'width': 434.40625, 'height': 81}
        return await element.screenshot(
            dict(type='png', omitBackground="transparency", clip=box))
        # {'type': 'png', 'fullPage': True, 'omitBackground': "transparency", "clip": box})
    else:
        return await page.screenshot(dict(type='png', fullPage=True, omitBackground="transparency"))


async def handle_to_png(browser, page_path, out_path, size, element_name=None):
    """
    截取成png格式图片
    :param browser:
    :param page_path:
    :param out_path:
    :param size:
    :param element_name:
    :return:
    """
    browser = browser or await init_browser()
    async with create_page(browser) as page:
        buffer = await to_buffer(page, out_path, size, element_name)
        with open(page_path, 'wb') as f:
            f.write(buffer)


async def handle_to_image(browser, page_path, size, element_name=None):
    """
    截取成 PIL Image 对象信息
    :param browser:
    :param page_path:
    :param size:
    :param element_name:
    :return:
    """
    browser = browser or await init_browser()
    async with create_page(browser) as page:
        buffer = await to_buffer(page, page_path, size, element_name)
        image = Image.open(BytesIO(buffer))
        return image


def asyncio_apply(func, *args, **kwargs):
    """
    执行协成操作
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    advocate_loop = asyncio.get_event_loop()
    return advocate_loop.run_until_complete(func(browser, *args, **kwargs))


if __name__ == "__main__":
    # handle_html(handle_to_png, "file:///Users/yangshujun/self/handle_css/test.html", "11.png", size=[1000, 1])
    #
    io_image_byte = BytesIO()
    img = asyncio_apply(handle_to_image, "file:///Users/yangshujun/self/handle_css/test.html", size=[1000, 1],
                        element_name="a")
    print(img.size)
    img.show()
    """
    import numpy as np
    import time

    print("end:", time.time() - start)
    print(img.mode)

    crop = np.asarray(img)
    print(len(crop))
    x = np.nonzero(crop[:, :, 3])
    c_min = min(x[1])
    c_max = max(x[1])
    r_min = min(x[0])
    r_max = max(x[0])
    crop = img.crop((c_min, r_min, c_max + 1, r_max + 1))
    print("end:", time.time() - start)
    crop.save("11.png")
    print("end:", time.time() - start)
    crop.show()
    """
