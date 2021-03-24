#
# xmindTool.py
# @author yanchunhuo
# @description 
# @created 2020-03-26T10:34:23.914Z+08:00
# @last-modified 2021-03-24T09:42:14.543Z+08:00
# @github https://github.com/yanchunhuo

from pojo.xmind.xmindData import XmindData
from pojo.xmind.sheet import Sheet
from pojo.xmind.rootTopic import RootTopic
from pojo.xmind.secondTopic import SecondTopic
from common.strTool import StrTool
import xmind
import os

class XmindTool:

    def __init__(self,filePath):
        self.filePath=filePath
        self.xfile=xmind.load(filePath)
        self.xmindData=XmindData()
        self._init()

    def _init(self):
        self.xmindData.fileName=os.path.basename(self.filePath)
        sheets=self.xfile.getSheets()
        for sheet in sheets:
            new_sheet=Sheet()
            new_rootTopic=RootTopic()
            new_sheet.sheetName=sheet.getTitle()
            rootTopic=sheet.getRootTopic()
            new_rootTopic.rootTopicName=rootTopic.getTitle()
            secondTopics=rootTopic.getSubTopics()
            if secondTopics:
                for secondTopic in secondTopics:
                    new_secondTopic = SecondTopic()
                    new_secondTopic.secondTopicName=secondTopic.getTitle()
                    data=self._dumpTopic(secondTopic)
                    new_secondTopic.data=data
                    new_rootTopic.secondTopics.append(new_secondTopic)
                new_sheet.rootTopic=new_rootTopic
            self.xmindData.sheets.append(new_sheet)

    def _dumpTopic(self, topic, tmp_result='', results=None):
        if results is None or not isinstance(results, list):
            results = []
        topic_title=topic.getTitle()
        if not topic_title is None:
            tmp_result += topic_title
        tmp_result += '--->'
        if topic.getMarkers():
            markerId=topic.getMarkers()[0].getMarkerId()
            tmp_result+=str(markerId)
        subTopics = topic.getSubTopics()
        if subTopics and len(subTopics):
            for subTopic in subTopics:
                self._dumpTopic(subTopic, tmp_result, results)
            tmp_result = ''
        if tmp_result:
            results.append(tmp_result[:-3])
        return results

    def getXmindData(self):
        return StrTool.objectToJson(self.xmindData)

    def count(self):
        """
        统计有多少个末尾节点
        :return: {'fileName':'fileName','num':'num','right_num':'right_num','wrong_num':'wrong_num'}
        """
        result={}
        xmindData=self.getXmindData()
        sheets=xmindData['sheets']
        tmp_sum = 0
        wrong_num = 0
        right_num = 0
        for sheet in sheets:
            rootTopic=sheet['rootTopic']
            if rootTopic:
                for secondTopic in rootTopic['secondTopics']:
                    tmp_sum+=len(secondTopic['data'])
                    for tmp_data in secondTopic['data']:
                        if 'symbol-wr' in tmp_data:
                            wrong_num += 1
                        if 'symbol-ri' in tmp_data:
                            right_num += 1
        result.update({'fileName':xmindData['fileName']})
        result.update({'num':tmp_sum})
        result.update({'right_num':right_num})
        result.update({'wrong_num':wrong_num})
        return result

    def countBySheet(self):
        """
        按sheet统计有多少个末尾节点
        :return: [{'sheetName':'sheetName','num':'num','right_num':'right_num','wrong_num':'wrong_num'}]
        """
        result=[]
        xmindData=self.getXmindData()
        sheets=xmindData['sheets']
        for sheet in sheets:
            tmp_result={}
            tmp_sum=0
            wrong_num = 0
            right_num = 0
            for secondTopic in sheet['rootTopic']['secondTopics']:
                tmp_sum+=len(secondTopic['data'])
                for tmp_data in secondTopic['data']:
                    if 'symbol-wr' in tmp_data:
                        wrong_num += 1
                    if 'symbol-ri' in tmp_data:
                        right_num += 1
            tmp_result.update({'sheetName':sheet['sheetName']})
            tmp_result.update({'num':tmp_sum})
            tmp_result.update({'right_num':right_num})
            tmp_result.update({'wrong_num':wrong_num})
            result.append(tmp_result)
        return result

    def countBySecondTopic(self):
        """
        按SecondTopic统计有多少个末尾节点
        :return: [{'sheetName':'sheetName','secondTopicName':'secondTopicName','num':'secondTopicName','right_num':'right_num','wrong_num':'wrong_num'}]
        """
        result=[]
        xmindData=self.getXmindData()
        sheets=xmindData['sheets']
        for sheet in sheets:
            for secondTopic in sheet['rootTopic']['secondTopics']:
                tmp_result = {}
                wrong_num = 0
                right_num = 0
                for tmp_data in secondTopic['data']:
                    if 'symbol-wr' in tmp_data:
                        wrong_num+=1
                    if 'symbol-ri' in tmp_data:
                        right_num+=1
                tmp_result.update({'sheetName':sheet['sheetName']})
                tmp_result.update({'secondTopicName':secondTopic['secondTopicName']})
                tmp_result.update({'num':len(secondTopic['data'])})
                tmp_result.update({'right_num':right_num})
                tmp_result.update({'wrong_num':wrong_num})
                result.append(tmp_result)
        return result