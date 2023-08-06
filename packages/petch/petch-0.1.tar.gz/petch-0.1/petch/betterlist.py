from typing import Any, Callable
from functools import reduce

class BetterList(list):
    '''
    This List Class allows you to do javascript styled continuous operation.
    ex.
    x = BetterList([1,2,3,4])
    y = x.filter(func1).map(func2).reduce(func3)
    z = x.map(func4).for_each(func5)
    '''
    @property
    def length(self):
        return len(self)

    def sort(self,func:Callable=lambda x:x):
        return BetterList(sorted(self,key=func))

    def min(self,func:Callable=lambda x:x,n_smallest:int=1):
        return BetterList(self.sort(func)[:n_smallest])

    def max(self,func:Callable=lambda x:x,n_largest:int=1):
        return BetterList(self.sort(func)[-n_largest:])
    
    def filter(self,func:Callable):
        return BetterList(filter(func,self))

    def filter_out(self,func:Callable):
        return BetterList(filter(lambda x: not(func(x)),self))

    def remove_duplicate(self):
        return BetterList(set(self))

    def map(self,func:Callable):
        return BetterList(map(func,self))
    
    def reduce(self,func:Callable):
        return reduce(func,self)

    def foreach(self,func:Callable):
        for x in self:
            func(x)

    def filter_index(self,func:Callable):
        _index = BetterList([i for i,_ in enumerate(self)])
        return BetterList([self[i] for i in _index.filter(func)])

    def get(self,index,default_value=None):
        try: return self[index]
        except IndexError: return default_value

    def value_after(self,value:Any):
        it = iter(self)
        x = ""
        while str(x) != str(value) or str(x) not in str(value):
            x=next(it)
        return next(it)

    def first(self,n:int):
        return BetterList(range(0,n)).map(lambda i: self[i])

    def last(self,n:int):
        return BetterList(range(-n,0)).map(lambda i: self[i])
