from pojo.xmind.xmindData import XmindData
from pojo.xmind.sheet import Sheet
from pojo.xmind.rootTopic import RootTopic
from pojo.xmind.secondTopic import SecondTopic
from common.strTool import StrTool
import xmind
import os

class XmindTool:

    def __init__(self,filePath):
        self._filePath=filePath
        self._xfile=xmind.load(filePath)
        self._xmindData=XmindData()
        self._init()

    def _init(self):
        self._xmindData.fileName=os.path.basename(self._filePath)
        sheets=self._xfile.getSheets()
        for sheet in sheets:
            new_sheet=Sheet()
            new_rootTopic=RootTopic()
            new_sheet.sheetName=sheet.getTitle()
            rootTopic=sheet.getRootTopic()
            new_rootTopic.rootTopicName=rootTopic.getTitle()
            secondTopics=rootTopic.getSubTopics()
            for secondTopic in secondTopics:
                new_secondTopic = SecondTopic()
                new_secondTopic.secondTopicName=secondTopic.getTitle()
                data=self._dumpTopic(secondTopic)
                new_secondTopic.data=data
                new_rootTopic.secondTopics.append(new_secondTopic)
            new_sheet.rootTopic=new_rootTopic
            self._xmindData.sheets.append(new_sheet)

    def _dumpTopic(self, topic, tmp_result='', results=None):
        if results is None or not isinstance(results, list):
            results = []
        tmp_result += topic.getTitle()
        tmp_result += '--->'
        subTopics = topic.getSubTopics()
        if subTopics and len(subTopics):
            for subTopic in subTopics:
                self._dumpTopic(subTopic, tmp_result, results)
            tmp_result = ''
        if tmp_result:
            results.append(tmp_result[:-3])
        return results

    def getXmindData(self):
        return StrTool.objectToJson(self._xmindData)

    def count(self):
        """
        统计有多少个末尾节点
        :return: [['fileName',num]]
        """
        result=[]
        xmindData=self.getXmindData()
        sheets=xmindData['sheets']
        tmp_sum = 0
        for sheet in sheets:
            for secondTopic in sheet['rootTopic']['secondTopics']:
                tmp_sum+=len(secondTopic['data'])
        result.append(xmindData['fileName'])
        result.append(tmp_sum)
        return result

    def countBySheet(self):
        """
        按sheet统计有多少个末尾节点
        :return: [['sheetName',num]]
        """
        result=[]
        xmindData=self.getXmindData()
        sheets=xmindData['sheets']
        for sheet in sheets:
            tmp_result=[]
            tmp_result.append(sheet['sheetName'])
            tmp_sum=0
            for secondTopic in sheet['rootTopic']['secondTopics']:
                tmp_sum+=len(secondTopic['data'])
            tmp_result.append(tmp_sum)
            result.append(tmp_result)
        return result

    def countBySecondTopic(self):
        """
        按SecondTopic统计有多少个末尾节点
        :return: [['sheetName','secondTopicName',num]]
        """
        result=[]
        xmindData=self.getXmindData()
        sheets=xmindData['sheets']
        for sheet in sheets:
            for secondTopic in sheet['rootTopic']['secondTopics']:
                tmp_result = []
                tmp_result.append(sheet['sheetName'])
                tmp_result.append(secondTopic['secondTopicName'])
                tmp_result.append(len(secondTopic['data']))
                result.append(tmp_result)
        return result
