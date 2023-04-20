from __future__ import annotations

import pandas as pd
from typing import Dict
from abc import ABC, abstractmethod
from typeguard import typechecked

import inspect
from decorator import decorator


@decorator
def multiDec(func, *args, **kwargs):
    call_args = inspect.getcallargs(func, *args, **kwargs)
    a = call_args.copy()
    a.pop('self').args = a
    return typechecked(func)(*args, **kwargs)

class ColumnGenerator(ABC):
    initDict: Dict[ColumnGenerator.__class__, int] = {}

    def __new__(cls, *args, **kwargs) -> ColumnGenerator:
        if ColumnGenerator.initDict.get(cls, None) is None:
            for name, m in inspect.getmembers(cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
                if name == '__init__':
                    if inspect.ismethod(m) or inspect.isfunction(m):
                        setattr(cls, name, multiDec(m))
            ColumnGenerator.initDict[cls] = 0

        instance = super(ColumnGenerator, cls).__new__(cls)
        return instance

    @abstractmethod
    def requires(self) -> Dict[str, ColumnGenerator]:
        pass

    @abstractmethod
    def gen(self, index, row: pd.Series):
        # open - The first traded price
        # high - The highest traded price
        # low - The lowest traded price
        # close - The final traded price
        # volume - The total volume traded by all trades
        # trades - The number of individual trades
        pass
        
    def __eq__(self, b) -> bool:
        return isinstance(self, type(b)) and self.args == b.args
    
    def __hash__(self):
        return hash((*self.args.values(),id(self.__class__),))