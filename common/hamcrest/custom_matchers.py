from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.hasmethod import hasmethod


class Is_True(BaseMatcher):
    def __init__(self) -> None:
        pass

    def _matches(self, item) -> bool:
        if item:
            return True
        else:
            return False
    
    def describe_to(self, description) -> None:
        description.append_text('True')
    
def h_is_true():
    return Is_True()

class Is_Empty(BaseMatcher):
    def __init__(self) -> None:
        pass

    def _matches(self, item) -> bool:
        if isinstance(item,str) or isinstance(item,tuple) or isinstance(item,list) or isinstance(item,set) or isinstance(item,dict):
            item_len=len(item)
            if len(item)>0:
                return False
            else:
                return True
        else:
            return False
    
    def describe_to(self, description) -> None:
        description.append_text('Empty')
        
def h_is_empty():
    return Is_Empty()