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
            for col_name, column_generator in self.colG.copy().items():
                renamed_dict = {}
                for defined_dependency_name, dependant_gen in column_generator.requires().items():
                    row_name = self.gCol.get(dependant_gen, None)
                    if row_name is None:
                        row_name = defined_dependency_name
                        self.addIterableColumn(row_name, dependant_gen)
                    
                    if row_name not in cache:
                        cache[row_name] = self.colG[row_name].gen(index, row)
                        row[row_name] = cache[row_name]

                    if not row_name == defined_dependency_name:
                        row.rename({row_name: defined_dependency_name}, inplace=True)
                        renamed_dict[defined_dependency_name] = row_name

                if col_name not in cache:
                    cache[col_name] = column_generator.gen(index, row) # dependencies has been gened gen col
                    row[col_name] = cache[col_name]

                row.rename(renamed_dict, inplace=True) #reverse renaming 
            yield index, row

