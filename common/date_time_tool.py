#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import calendar
import datetime
import time

class DateTimeTool:
    @classmethod
    def get_now_time(cls, format='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.now().strftime(format)

    @classmethod
    def get_now_date(cls, format='%Y-%m-%d'):
        return datetime.date.today().strftime(format)

    @classmethod
    def get_now_year(cls, format='%Y'):
        return datetime.date.today().strftime(format)

    @classmethod
    def get_now_timestamp_with_second(cls):
        return int(time.time())

    @classmethod
    def get_now_timestamp_with_millisecond(cls):
        return int(round(time.time() * 1000))

    @classmethod
    def timestamp_to_datetime(cls, timeStamp: int, is_with_millisecond=False):
        if is_with_millisecond:
            timeStamp = timeStamp / 1000
        resultDateTime = datetime.datetime.fromtimestamp(timeStamp)
        return resultDateTime

    @classmethod
    def str_to_timestamp(cls, str, str_format: str = '%Y-%m-%d %H:%M:%S', is_with_millisecond=False):
        dst_dateTime = datetime.datetime.strptime(str, str_format)
        if is_with_millisecond:
            timestamp = int(time.mktime(dst_dateTime.timetuple()) * 1000)
        else:
            timestamp = int(time.mktime(dst_dateTime.timetuple()))
        return timestamp

    @classmethod
    def time_to_timestamp(cls, date_time, is_with_millisecond=False):
        if is_with_millisecond:
            timestamp = int(time.mktime(date_time.timetuple()) * 1000)
        else:
            timestamp = int(time.mktime(date_time.timetuple()))
        return timestamp

    @classmethod
    def get_weekday(cls):
        """
        获得今天星期几，从1开始
        :return:
        """
        return datetime.datetime.now().weekday() + 1
    
    @classmethod
    def get_today_in_weekday(self, currentday=None):
        """
        按数值（1-7）返回今天是周几的英文
        :return:
        """
        if currentday == None:
            currentday = self.get_weekday()
        if currentday == 1:
            weekday = "Monday"
        elif currentday == 2:
            weekday = "Tuesday"
        elif currentday == 3:
            weekday = "Wednesday"
        elif currentday == 4:
            weekday = "Thursday"
        elif currentday == 5:
            weekday = "Friday"
        elif currentday == 6:
            weekday = "Saturday"
        else:
            weekday = "Sunday"
        return weekday
    
    @classmethod
    def get_how_second_ago(cls,nowDateTime, nowDateTime_format='%Y-%m-%d %H:%M:%S', howSecondAgo=0,
                      resultDateTime_format='%Y-%m-%d %H:%M:%S')->str:
        nowDateTime = datetime.datetime.strptime(nowDateTime, nowDateTime_format)
        resultDateTime = nowDateTime - datetime.timedelta(seconds=howSecondAgo)
        resultDateTime = resultDateTime.strftime(resultDateTime_format)
        return resultDateTime
    
    @classmethod
    def get_how_minutes_ago(cls,nowDateTime, nowDateTime_format='%Y-%m-%d %H:%M:%S', howMinutesAgo=0,
                      resultDateTime_format='%Y-%m-%d %H:%M:%S')->str:
        nowDateTime = datetime.datetime.strptime(nowDateTime, nowDateTime_format)
        resultDateTime = nowDateTime - datetime.timedelta(minutes=howMinutesAgo)
        resultDateTime = resultDateTime.strftime(resultDateTime_format)
        return resultDateTime

    @classmethod
    def get_how_days_Ago(cls, nowDateTime, nowDateTime_format='%Y-%m-%d %H:%M:%S', howDaysAgo=0,
                      resultDateTime_format='%Y-%m-%d %H:%M:%S')->str:
        nowDateTime = datetime.datetime.strptime(nowDateTime, nowDateTime_format)
        resultDateTime = nowDateTime - datetime.timedelta(days=howDaysAgo)
        resultDateTime = resultDateTime.strftime(resultDateTime_format)
        return resultDateTime

    @classmethod
    def get_how_days_future(cls, nowDateTime, nowDateTime_format='%Y-%m-%d %H:%M:%S', howDaysFuture=0,
                         resultDateTime_format='%Y-%m-%d %H:%M:%S'):
        nowDateTime = datetime.datetime.strptime(nowDateTime, nowDateTime_format)
        resultDateTime = nowDateTime + datetime.timedelta(days=howDaysFuture)
        resultDateTime = resultDateTime.strftime(resultDateTime_format)
        return resultDateTime

    @classmethod
    def get_how_years_ago(cls, nowDate, howYearsAgo=0, nowDate_format='%Y-%m-%d'):
        nowDateTime = datetime.datetime.strptime(nowDate, nowDate_format)
        resultDate = nowDateTime - datetime.timedelta(days=howYearsAgo * 366)
        return resultDate

    @classmethod
    def date_time_to_str(cls, theDateTime, format='%Y-%m-%d'):
        return theDateTime.strftime(format)

    @classmethod
    def str_to_date_time(cls, str, str_format: str = '%Y-%m-%d %H:%M:%S'):
        dst_dateTime = datetime.datetime.strptime(str, str_format)
        return dst_dateTime

    @classmethod
    def get_monday_date_by_any_date(cls, dateTime, dateTime_format='%Y-%m-%d %H:%M:%S'):
        dateTime = datetime.datetime.strptime(dateTime, dateTime_format)
        while (not dateTime.weekday() == 0):
            dateTime = dateTime - datetime.timedelta(days=1)
        return cls.date_time_to_str(dateTime, dateTime_format)

    @classmethod
    def get_current_month_first_day_or_last_day(cls, type=1):
        """获取当前月第一天或者最后一天日期

        Args:
            type (int, optional): 第一天:1，最后一天:-1

        Returns:
            [type]: [description]
        """
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        last_day = calendar.monthrange(year, month)[1]
        if type == 1:
            start = datetime.date(year, month, 1)
            return start
        if type == -1:
            end = datetime.date(year, month, last_day)
            return end

    @classmethod
    def time_cmp(self, systemtime=None, parmatime=None, format="%H%M"):
        """
        :param systemtime:默认系统时间
        :param parmatime:默认系统时间
        :param format:比对格式
        :return:state
        0：系统时间大于当前时间、1：系统时间等于当前时间、2：系统时间小于当前时间
        """
        # 传入时间与当前系统时间比对，根据参数：format进行哪些字段比较
        if systemtime == None:
            systemtime = int(time.strptime(DateTimeTool.get_now_time(format), format))
        if parmatime == None:
            parmatime = int(time.strptime(DateTimeTool.get_now_time(format), format))
        time1 = int(time.strftime(format, systemtime))
        time2 = int(time.strftime(format, parmatime))
        if time1 > time2:
            state = 0
        elif time1 == time2:
            state = 1
        else:
            state = 2
        return state

    @classmethod
    def get_str_date_to_format_date(self, strday=None, split_type="-"):
        """
        根据(年月日)日期分割返回格式化后的日期
        :param strday: 自定义年月日
        :param split_type: 自定义分割符
        :return:
        """
        y, m, d = strday.split(split_type)
        falmt_date = datetime.date(int(y), int(m), int(d))
        return falmt_date

    def get_timestamp_with_spec_time(days: int = 0, hour: int = None, minute: int = 0, second: int = 0,
                                is_with_millisecond=True):
        """
        获取指定的时间点的时间戳
        :param days:  与当前时间的相差的天数。-1 表示昨天；0 表示当天(默认)；1 表示明天
        :param hour: 时;指定的时间,比如当天的凌晨一点,时即为1(24小时制)
        :param minute: 分;指定的时间,比如当天某小时的1分钟,分即为1(24小时制)
        :param second: 秒;指定的时间,比如当天的某小时的某分钟1秒,秒即为1(24小时制)
        :return:      返回时间戳
        """
        nowTime = datetime.datetime.now() + datetime.timedelta(days=days)
        specified_time = nowTime.strftime("%Y-%m-%d") + " {}:{}:{}".format(hour, minute, second)
        timeArray = time.strptime(specified_time, "%Y-%m-%d %H:%M:%S")
        if is_with_millisecond:
            specified_time_stamp = int(time.mktime(timeArray)) * 1000
        else:
            specified_time_stamp = int(time.mktime(timeArray))
        return specified_time_stamp