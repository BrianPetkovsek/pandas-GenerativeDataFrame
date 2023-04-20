import pandas as pd
from typing import Dict
import numpy as np
from ..ColumnGenerator import ColumnGenerator


class SMAGenerator(ColumnGenerator):

    def __init__(self, window_size) -> None:
        self.window_size = window_size
        self.close_values = []
        self.close_sum = 0

    def requires(self) -> Dict[str, ColumnGenerator]:
        return {}    

    def gen(self, index, row: pd.Series):
        # open - The first traded price
        # high - The highest traded price
        # low - The lowest traded price
        # close - The final traded price
        # volume - The total volume traded by all trades
        # trades - The number of individual trades
        open = row.open
        high = row.high
        low = row.low
        close = row.close
        volume = row.volume
        #trades = row.trades

        # Append close value to close_values and update close_sum
        self.close_values.append(close)
        self.close_sum += close
        
        # Check if close_values has more than window_size values, remove oldest value if needed and update close_sum
        if len(self.close_values) > self.window_size:
            self.close_sum -= self.close_values.pop(0)
        else:
            return np.NaN
        
        close_sma = self.close_sum/self.window_size

        return close_sma