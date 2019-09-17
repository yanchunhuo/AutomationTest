#-*- coding:utf8 -*-
import datetime
import time

class DateTimeTool:
    @classmethod
    def getNowTime(cls,format='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.now().strftime(format)

    @classmethod
    def getNowDate(cls,format='%Y-%m-%d'):
        return datetime.date.today().strftime(format)

    @classmethod
    def getNowTimeStampWithSecond(cls):
        return int(time.time())

    @classmethod
    def getNowTimeStampWithMillisecond(cls):
        return int(round(time.time()*1000))

    @classmethod
    def getHowDaysAgo(cls,nowDateTime,nowDateTime_format='%Y-%m-%d %H:%M:%S',howDaysAgo=0):
        nowDateTime = datetime.datetime.strptime(nowDateTime, nowDateTime_format)
        resultDateTime=nowDateTime-datetime.timedelta(days=howDaysAgo)
        return resultDateTime

    @classmethod
    def dateTimeToStr(cls,theDateTime,format='%Y-%m-%d'):
        return theDateTime.strftime(format)

    @classmethod
    def getHowYearsAgo(cls,nowDate,howYearsAgo=0,nowDate_format='%Y-%m-%d'):
        resultDate = cls.getHowDaysAgo(nowDate,nowDate_format,howYearsAgo*366)
        return resultDate