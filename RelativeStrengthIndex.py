import numpy as np
import pandas as pd

class RelativeStrengthIndex:
    def __init__(self, lookback: int):
        self._lb = lookback
        self._au = np.nan
        self._ad = np.nan
        self._curr_rsi = np.nan
        self.custom_rsi = []

    def update(self, i: int, time_index: pd.DatetimeIndex, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray):
        if i < self._lb-1:
            self.custom_rsi.append(np.nan)
            return
        else:
            price_changes = close[i-self._lb:i+1] - open[i-self._lb:i+1]
            self._au = np.sum(np.where(price_changes > 0, price_changes, 0))
            self._ad = np.sum(np.where(price_changes < 0, -price_changes, 0))

            if self._ad == 0:
                self._curr_rsi = 100
            else:
                rs = self._au / self._ad
                self._curr_rsi = 100 - (100 / (1 + rs))
            self.custom_rsi.append(self._curr_rsi)