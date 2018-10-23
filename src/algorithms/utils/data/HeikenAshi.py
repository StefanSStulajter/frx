#
# This utility creates Heiken Ashi series from the input
# The series is trying to capture momentum in a better way compared to standard candles
#
# Heiken Ashi OHLC is calcualted as following:
# HAClose = (open + high + low + close) / 4
# HAOpen = (HAOpen[previous] + HAClose[previous]) / 2
# HAHigh = max(high, HAOpen, HAClose)
# HALow = min (low, HAOpen, HAClose)
#

import numpy as np
import pandas as pd

# @param prices:    Pandas dataframe containing OHLC data
# @param periods:   list of time periods for which we want to calculate the Heiken Ashi series
# @return:          Heiken Ashi OHLC series

def build(prices, periods):
    dictionary = {}

    for i in range(0, len(periods)):
        HAClose = prices[["open", "high", "low", "close"]].sum(axis=1) / 4
        HAOpen = HAClose.copy()
        HAOpen.iloc[0] = HAClose.iloc[0]
        HAHigh = HAClose.copy()
        HALow = HAClose.copy()

        for j in range(1, len(prices)):
            HAOpen.iloc[j] = (HAOpen.iloc[j-1] + HAClose.iloc[j-1]) / 2
            HAHigh.iloc[j] = np.array([prices.high.iloc[j], HAOpen.iloc[j], HAClose.iloc[j]]).max()
            HALow.iloc[j] = np.array([prices.low.iloc[j], HAOpen.iloc[j], HAClose.iloc[j]]).min()

        df = pd.concat((HAOpen, HAHigh, HALow, HAClose), axis=1)

        df.columns = ["open", "high", "low", "close"]

        dictionary[periods[i]] = df
    
    return dictionary