import pandas as pd
from PandasGenerativeDataFrame.Generators import SMAGenerator
from PandasGenerativeDataFrame import ColumnGenerator
from typing import Dict

class ExampleRequiresGen(ColumnGenerator):
    def __init__(self) -> None:
        pass

    def requires(self) -> Dict[str, ColumnGenerator]:
        return {"SMA_10": SMAGenerator(10)}
    
    def gen(self, index, row: pd.Series):
        return row.SMA_10+1

