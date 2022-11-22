#
# imageCompare.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2020-02-26T13:47:34.255Z+08:00
# @last-modified 2022-11-21T18:05:58.930Z+08:00
#

from skimage.io import imread
from skimage.metrics import structural_similarity
from skimage.transform import resize

class ImageCompare:
    @classmethod
    def compareTwoImage(cls,image1_path,image2_path,zoom_type='out'):
        """
        比较两张图片相识度,返回值范围为0~1,提供比较的两张图片尺寸应该一致,如果不一致会进行缩放
        :param image1_path:
        :param image2_path:
        :param zoom_type: in:放大,out:缩小,当图片尺寸一致时,该参数被忽略
        :return:
        """
        image1_ndarray=imread(image1_path)
        image2_ndarray=imread(image2_path)
        height1,width1,channel1=image1_ndarray.shape
        height2,width2,channel2=image2_ndarray.shape
        if not height1==height2 or not width1==width2:
            height=0
            width=0
            if zoom_type.lower()=='in':
                height=max(height1,height2)
                width=max(width1,width2)
            elif zoom_type.lower()=='out':
                height=min(height1,height2)
                width=min(width1,width2)
            image1_ndarray = resize(image1_ndarray,(height,width,channel1))
            image2_ndarray = resize(image2_ndarray, (height, width,channel2))
        score,diff=structural_similarity(image1_ndarray,image2_ndarray,full=True,channel_axis=1,multichannel=True)
        return score