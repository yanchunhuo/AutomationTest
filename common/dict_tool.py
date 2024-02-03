# @Author  : yanchunhuo
# @Time    : 2020/4/15 11:01

class DictTool:
    @classmethod
    def sorted_dict_in_list(cls, datas):
        """
        将数组内的字典按字母进行排序
        :param datas:
        :return:
        """
        new_datas = []
        for data in datas:
            new_data = {}
            for key in sorted(data):
                new_data.update({key: data[key]})
            new_datas.append(new_data)
        return new_datas

    @classmethod
    def sorted_dict(cls,data):
        list = []
        for key in data:
            list.append(key)
        data_result = {}
        list.sort()
        for i in list:
            data_result[i] = data[i]
        return data_result

