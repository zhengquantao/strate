from strate.strategy_base import Strategy
from strate.utils import assert_msg, crossover, SMA


class SmaCross(Strategy):
    # 小窗口SMA的窗口大小，用于计算SMA快线
    fast = 30

    # 大窗口SMA的窗口大小，用于计算SMA慢线
    slow = 90

    def init(self):
        # 计算历史上每个时刻的快线和慢线
        self.sma1 = self.I(SMA, self.data.Close, self.fast)
        self.sma2 = self.I(SMA, self.data.Close, self.slow)
        print(self.sma1)
        print(self.sma2)

    def next(self, tick):
        # 如果此时快线刚好越过慢线，买入全部
        if crossover(self.sma1[:tick], self.sma2[:tick]):
            self.buy()

        # 如果是慢线刚好越过快线，卖出全部
        elif crossover(self.sma2[:tick], self.sma1[:tick]):
            self.sell()

        # 否则，这个时刻不执行任何操作。
        else:
            pass