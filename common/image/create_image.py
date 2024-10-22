#
# create_image.py
# @author yanchunhuo
# @description 
# @created 2024-10-22T11:11:39.448Z+08:00
# @last-modified 2024-10-22T11:26:07.993Z+08:00
# @github https://github.com/yanchunhuo
# 

from PIL import Image
import os

class CreateImage:
    
    @classmethod
    def create_image_with_size(cls,store_file_path, image_size, width, height,color='green'):
        """_summary_

        Args:
            store_file_path (_type_): _description_
            image_size (_type_): 字节大小
            width (_type_): _description_
            height (_type_): _description_
            color (_type_): red、yellow、blue、black、white、green
        """
        # 创建一个新图片
        image = Image.new('RGB', (width, height), color)
        
        # 保存图片到临时文件
        temp_file_path = store_file_path + '.tmp'
        image.save(temp_file_path, 'JPEG', quality=100)  # 使用最高质量以最小化文件大小
        
        # 获取临时文件的大小
        file_size = os.path.getsize(temp_file_path)
        
        # 如果文件大小小于目标大小，则填充数据
        if file_size < image_size:
            with open(temp_file_path, 'rb') as f:
                data = f.read()
            
            # 计算需要填充的数据量
            padding_size = image_size - file_size
            padding_data = b'\0' * padding_size
            
            # 填充数据并写回文件
            with open(temp_file_path, 'wb') as f:
                f.write(data)
                f.write(padding_data)
        
        # 重命名临时文件为目标文件
        os.replace(temp_file_path, store_file_path)