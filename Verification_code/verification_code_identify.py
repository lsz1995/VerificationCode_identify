# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image


def initTable(threshold=100):  # 二值化函数
    table = []
    for i in range(256):
        if i > threshold:
            table.append(0)
        else:
            table.append(1)

    return table


def print_bin(img):
    """
    输出二值后的图片到控制台，方便调试的函数
    :param img:
    :type img: Image
    :return:
    """
    print('current binary output,width:%s-height:%s\n')
    for h in range(img.height):
        for w in range(img.width):
            value = img.getpixel((w,h))
            if value == 0:
                print(value, end='')
            else:
                print(' ', end='')

        print('')


def get_captcha(path):
    im = Image.open(path)  # 1.打开图片
    im = im.convert('L')
    binaryImage = im.point(initTable(), '1')
    binaryImage.show()
    text = pytesseract.image_to_string(binaryImage, config='-psm 7')
    print(text)
    return text


def sum_9_region_new(img, x, y):
    # 确定噪点
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    # 因当前图片的四周都有黑点，所以周围的黑点可以去除
    if y < 3:  # 本例中，前两行的黑点都可以去除
        return 1
    elif y > height - 3:  # 最下面两行
        return 1
    else:  # y不在边界
        if x < 3:  # 前两列
            return 1
        elif x == width - 1:  # 右边非顶点
            return 1
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum


def collect_noise_point(img):
    # 收集所有的噪点
    noise_point_list = []
    for x in range(img.width):
        for y in range(img.height):
            res_9 = sum_9_region_new(img, x, y)
            if (0 < res_9 < 3) and img.getpixel((x, y)) == 0:  # 找到孤立点
                pos = (x, y)
                noise_point_list.append(pos)
    return noise_point_list


def remove_noise_pixel(img, noise_point_list):
    # 根据噪点的位置信息，消除二值图片的黑点噪声
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)


def noise_reduction(img):
    """
    :param img: 灰度处理 二值化 后的图片
    :return:
    """
    noise_point_list = collect_noise_point(img)  # 收集噪点
    remove_noise_pixel(img, noise_point_list)  # 去除噪点
    print_bin(img)  # 输出二值图像
    return img


if __name__ == '__main__':
    path = "6.png"

    im = Image.open(path)  # 1.打开图片

    im = im.convert('L')
    binaryImage = im.point(initTable(), '1')

    binaryImage = noise_reduction(binaryImage)

    text = pytesseract.image_to_string(binaryImage, lang='eng')

    print(text)


