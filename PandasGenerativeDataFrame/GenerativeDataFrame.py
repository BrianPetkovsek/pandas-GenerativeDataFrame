import pandas as pd
from typing import Dict
from typing import Iterable
from typing import Hashable
from typing import Tuple
from .ColumnGenerator import ColumnGenerator
from typeguard import typechecked

@typechecked
class GenerativeDataFrame:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df: pd.DataFrame = df
        self.colG: Dict[str, ColumnGenerator] = {}
        self.gCol: Dict[ColumnGenerator, str] = {}
    
    def addIterableColumn(self, column_name: str, columnGenerator: ColumnGenerator):
       self.colG[column_name] = columnGenerator
       self.gCol[columnGenerator] = column_name
       
    
    def removeIterableColumn(self, column: str):
        gen = self.colG.pop(column)
        self.gCol.pop(gen)
    
    def iterrows(self) -> Iterable[Tuple[Hashable, pd.Series]]:
        for index, row in self.df.iterrows():
            cache = {}
            dependency_queue = []
            for col_name, column_generator in self.colG.copy().items():
                dependency_queue.append({column_generator: col_name})
                while dependency_queue:
                    dependency = dependency_queue.pop(0)
                    for dependant_gen, defined_dependency_name in dependency.items():
                        req = dependant_gen.requires()
                        if req and (req.keys()-cache):
                            dependency_queue.append(req)
                            dependency_queue.append(dependency)
                            continue

                        for gen, name in req.items():
                            row.rename({cache[gen]: name}, inplace=True)
                        
                        if dependant_gen not in self.gCol:
                            self.addIterableColumn(defined_dependency_name, dependant_gen)
                        if dependant_gen not in cache: 
                            row[defined_dependency_name] = self.colG[defined_dependency_name].gen(index, row)
                            cache[dependant_gen] = defined_dependency_name

            for gen, name in self.gCol.items():
                row.rename({cache[gen]: name}, inplace=True)
            yield index, row

