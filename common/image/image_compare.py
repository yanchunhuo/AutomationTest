#
# image_compare.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2020-02-26T13:47:34.255Z+08:00
# @last-modified 2024-08-21T19:05:44.907Z+08:00
#

from skimage.color import rgb2gray
from skimage.io import imread
from skimage.metrics import structural_similarity
from skimage.transform import resize

class ImageCompare:
    @classmethod
    def compareTwoImage(cls,image1_path,image2_path,zoom_type='out',convert_to_gray=True):
        """
        比较两张图片相识度,返回值范围为0~1,提供比较的两张图片尺寸应该一致,如果不一致会进行缩放
        :param image1_path:
        :param image2_path:
        :param zoom_type: in:放大,out:缩小,当图片尺寸一致时,该参数被忽略
        :param convert_to_gray: 是否将图片转换为灰度图
        :return:
        """
        # 图片比对保障图片类型（RGB/灰色）一致、通道数一致、尺寸一致、形状一致
        image1_ndarray=imread(image1_path)
        image2_ndarray=imread(image2_path)
        
        # 统一图片类型为灰度图
        if convert_to_gray:
            # RGB格式彩色图
            if len(image1_ndarray.shape)==3 and image1_ndarray.shape[2]==3:
                image1_ndarray=rgb2gray(image1_ndarray)
            # RGBA格式彩色图，先转为RGB再转为灰度图
            elif len(image1_ndarray.shape)==3 and image1_ndarray.shape[2]==4:
                image1_ndarray=image1_ndarray[:,:,:3]
                image1_ndarray=rgb2gray(image1_ndarray)
            # 灰度图
            else:
                pass
            # RGB格式彩色图
            if len(image2_ndarray.shape)==3 and image2_ndarray.shape[2]==3:
                image2_ndarray=rgb2gray(image2_ndarray)
            # RGBA格式彩色图，先转为RGB再转为灰度图
            elif len(image2_ndarray.shape)==3 and image2_ndarray.shape[2]==4:
                image2_ndarray=image2_ndarray[:,:,:3]
                image2_ndarray=rgb2gray(image2_ndarray)
            # 灰度图
            else:
                pass
        height1,width1=image1_ndarray.shape[:2]
        height2,width2=image2_ndarray.shape[:2]
        if not height1==height2 or not width1==width2:
            height=0
            width=0
            if zoom_type.lower()=='in':
                height=max(height1,height2)
                width=max(width1,width2)
            elif zoom_type.lower()=='out':
                height=min(height1,height2)
                width=min(width1,width2)
            # anti_aliasing=True 减少锯齿效果
            image1_ndarray = resize(image1_ndarray,(height,width),anti_aliasing=True)
            image2_ndarray = resize(image2_ndarray, (height, width),anti_aliasing=True)
        score,diff=structural_similarity(image1_ndarray,image2_ndarray,full=True,channel_axis=None if convert_to_gray else -1)
        return score