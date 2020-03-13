# 作者 yanchunhuo
# 创建时间 2020/2/26 10:00
# github https://github.com/yanchunhuo
from skimage.metrics import structural_similarity
import cv2

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
        image1=cv2.imread(image1_path)
        image2=cv2.imread(image2_path)
        height1,width1,channel1=image1.shape
        height2,width2,channel2=image2.shape
        if not height1==height2 or not width1==width2:
            height=0
            width=0
            if zoom_type.lower()=='in':
                height=max(height1,height2)
                width=max(width1,width2)
            elif zoom_type.lower()=='out':
                height=min(height1,height2)
                width=min(width1,width2)
            image1 = cv2.resize(image1, (height, width))
            image2 = cv2.resize(image2, (height, width))
        image1_gray=cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
        image2_gray=cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        score,diff=structural_similarity(image1_gray,image2_gray,full=True,multichannel=True)
        return score