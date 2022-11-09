#
# hamcrest.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2022-11-08T18:13:31.156Z+08:00
# @last-modified 2022-11-09T17:04:40.225Z+08:00
#

from hamcrest import assert_that as h_assert_that,equal_to,has_length,has_property,has_properties,none,not_none
from hamcrest import is_not,not_,all_of,any_of,anything
from hamcrest import close_to,greater_than,greater_than_or_equal_to,less_than,less_than_or_equal_to
from hamcrest import contains_string,string_contains_in_order,starts_with,ends_with,equal_to_ignoring_case,equal_to_ignoring_whitespace,matches_regexp
from hamcrest import contains,contains_inanyorder,only_contains,has_item,has_items,is_in,empty
from hamcrest import has_entries,has_entry,has_key,has_value
from hamcrest import is_
from .custom_matchers import h_is_true,h_is_empty

def assert_that(value:object):
    __assert=__Assert()
    __assert.value=value
    return __assert
    
class __Assert:
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, ):
        if self.__inited is None:
            self.value=None
            self.__inited = True

    ######################### Object #########################
    def is_equal_to(self,expected_value,reason:str=''):
        """对象是否相等

        Args:
            expected_value (_type_): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,equal_to(expected_value),reason=reason)
    
    def is_not_equal_to(self,expected_value,reason:str=''):
        """对象是否不相等

        Args:
            expected_value (_type_): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,is_not(equal_to(expected_value)),reason=reason)
    
    def is_length(self,len:int,reason:str=''):
        """对象长度是否符合预期

        Args:
            len (int): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,has_length(len),reason=reason)
        
    def has_property(self,property_name:str,reason:str=''):
        """对象是否包含某一个属性

        Args:
            property_name (str): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,has_property(property_name),reason=reason)
        
    def has_properties(self,property_names:list,reason:str=''):
        """对象是否包含给予的所有属性

        Args:
            property_names (list): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        for property_name in property_names:
            self.has_property(property_name=property_name,reason=reason)
    
    def has_properties_and_values(self,properties_and_values:dict,reason:str=''):
        """对象的属性和值是否等于给予的所有属性和值

        Args:
            properties_and_values (dict): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,has_properties(properties_and_values),reason=reason)
        
    def is_none(self,reason:str=''):
        h_assert_that(self.value,none(),reason=reason)
    
    def is_not_none(self,reason:str=''):
        h_assert_that(self.value,not_none(),reason=reason)
    
    def is_empty(self,reason:str=''):
        h_assert_that(self.value,h_is_empty(),reason=reason)
        
    def is_not_empty(self,reason:str=''):
        h_assert_that(self.value,is_not(h_is_empty()),reason=reason)
    
    ######################### Number #########################
    def is_close_to(self,expected_value:float,maxinum_delta:float,reason:str=''):
        """两个数相差是否在最大的差值范围内

        Args:
            expected_value (float): _description_
            maxinum_delta (float): 最大差值
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,close_to(expected_value,maxinum_delta),reason=reason)
    
    def is_greater_than(self,expected_value,reason:str=''):
        h_assert_that(self.value,greater_than(expected_value),reason=reason)
        
    def is_greater_than_or_equal_to(self,expected_value,reason:str=''):
        h_assert_that(self.value,greater_than_or_equal_to(expected_value),reason=reason)
        
    def is_less_than(self,expected_value,reason:str=''):
        h_assert_that(self.value,less_than(expected_value),reason=reason)
        
    def is_less_than_or_equal_to(self,expected_value,reason:str=''):
        h_assert_that(self.value,less_than_or_equal_to(expected_value),reason=reason)
        
    ######################### Text #########################
    def contains(self,substring:str,reason:str=''):
        h_assert_that(self.value,contains_string(substring),reason=reason)
    
    def does_not_contains(self,substring:str,reason:str=''):
        h_assert_that(self.value,is_not(contains_string(substring)),reason=reason)
        
    def contains_in_order(self,substrings:list,reason:str=''):
        """字符串是否按顺序匹配数组内的子串

        Args:
            substrings (list): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,string_contains_in_order(*substrings),reason=reason)
        
    def starts_with(self,substring:str,reason:str=''):
        h_assert_that(self.value,starts_with(substring),reason=reason)
    
    def ends_with(self,substring:str,reason:str=''):
        h_assert_that(self.value,ends_with(substring),reason=reason)
        
    def is_equal_to_ignoring_case(self,string:str,reason:str=''):
        h_assert_that(self.value,equal_to_ignoring_case(string),reason=reason)
    
    def is_equal_to_ignoring_whitespace(self,string:str,reason:str=''):
        """忽略前后空格的比较

        Args:
            string (str): _description_
            reason (str, optional): _description_. Defaults to ''.
        """
        h_assert_that(self.value,equal_to_ignoring_whitespace(string),reason=reason)
    
    def is_match_by_regexp(self,pattern:str,reason:str=''):
        h_assert_that(self.value,matches_regexp(pattern),reason=reason)
        
    ######################### Logical #########################
    def is_false(self,reason:str=''):
        h_assert_that(self.value,is_not(h_is_true()),reason=reason)
    
    def is_true(self,reason:str=''):
        h_assert_that(self.value,is_(h_is_true()),reason=reason)
    
    ######################### Sequence #########################
        
    def is_in(self,sequence:list,reason:str=''):
        h_assert_that(self.value,is_in(sequence),reason=reason)
    
    def is_not_in(self,sequence:list,reason:str=''):
        h_assert_that(self.value,is_not(is_in(sequence)),reason=reason)
        
    def is_has_item(self,expected_value,reason:str=''):
        h_assert_that(self.value,has_item(expected_value),reason=reason)
    
    def is_has_items(self,expected_values:list,reason:str=''):
        h_assert_that(self.value,has_items(*expected_values),reason=reason)
        
    def is_empty_sequence(self,reason:str=''):
        h_assert_that(self.value,empty(),reason=reason)
    ######################### Dictionary #########################
    def contains_key(self,key:str,reason:str=''):
        h_assert_that(self.value,has_key(key),reason=reason)
    
    def contains_keys(self,keys:list,reason:str=''):
        has_keys=[]
        for key in keys:
            has_keys.append(has_key(key))
        h_assert_that(self.value,all_of(*has_keys),reason=reason)
        
    def contains_value(self,value,reason:str=''):
        h_assert_that(self.value,has_value(value),reason=reason)
        
    def contains_values(self,values:list,reason:str=''):
        has_values=[]
        for value in values:
            has_values.append(has_value(value))
        h_assert_that(self.value,all_of(*has_values),reason=reason)
    
    def contains_entry(self,key:str,value,reason:str=''):
        h_assert_that(self.value,has_entry(key,value),reason=reason)
    
    def contains_entries(self,entries:dict,reason:str=''):
        h_assert_that(self.value,has_entries(entries),reason=reason)
        
    ######################### Decorator #########################
    
    