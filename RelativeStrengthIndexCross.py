import numpy as np
import pandas as pd
from RelativeStrengthIndex import RelativeStrengthIndex
from LocalRecord import LocalRecord
from copy import copy

class RelativeStrengthIndexCross:
    def __init__(self, lookback_1: int, lookback_2: int, direction: int):
        self.rsi_1 = RelativeStrengthIndex(lookback_1)
        self.rsi_2 = RelativeStrengthIndex(lookback_2)
        self._direction = direction

        self._pending_trade = None
        self.trading_records = []
    
    def _create_entries(self, i: int, time_index: pd.DatetimeIndex, open: np.ndarray, trade_type: int):
        new_contract = LocalRecord(entry_index=i, entry_price=open[i], entry_timestamp=time_index[i], exit_index=-1, exit_price=np.nan, exit_timestamp=time_index[i], trade_type=trade_type, percentage_change=np.nan)
        self._pending_trade = new_contract

    def _create_exites(self, i: int, time_index: pd.DatetimeIndex, open: np.ndarray, trade_type: int):
        assert self._pending_trade.trade_type == trade_type

        self._pending_trade.exit_index = i
        self._pending_trade.exit_price = open[i]
        self._pending_trade.exit_timestamp = time_index[i]
        self._pending_trade.percentage_change = (self._pending_trade.exit_price - self._pending_trade.entry_price) * self._pending_trade.trade_type / self._pending_trade.entry_price * 100
        
        self.trading_records.append(copy(self._pending_trade))
        self._pending_trade = None

    def update(self, i: int, time_index: pd.DatetimeIndex, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray):
        if i >= np.max([self.rsi_1._lb, self.rsi_2._lb]):
            if self._pending_trade == None:
                if self.rsi_1._curr_rsi > self.rsi_2._curr_rsi:
                    self._create_entries(i, time_index, open, 1)
            else:
                if self.rsi_2._curr_rsi > self.rsi_1._curr_rsi:
                    self._create_exites(i, time_index, open, 1)


        self.rsi_1.update(i, time_index, open, high, low, close)
        self.rsi_2.update(i, time_index, open, high, low, close)