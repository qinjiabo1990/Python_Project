"""
    
    __author__ =
    student number =
    __email__ = 
"""

import stocks
from collections import deque


class LoadCSV(stocks.Loader):
    """ loads stock market data from files that are in a comma-separate format."""

    def _process(self, file):
        try:
            for line in file:
                row = line.strip().split(',')
                # row[0 : 6]: stock_code,date,opening_price,high_price,low_price,closing_price,volume
                trading_data = stocks.TradingData(row[1], float(row[2]), float(row[3]),
                                                  float(row[4]), float(row[5]), int(row[6]))
                stock = self._stocks.get_stock(row[0])
                stock.add_day_data(trading_data)
        except Exception as e:
            raise RuntimeError("invalid format!")


class LoadTriplet(stocks.Loader):
    """loads stock market data from files that are in a triplet key-coded format."""

    def _add_stock(self, lines):
        """
        get lines's information and create new Stock adding in stock_collection
        :param lines: list
        :return: Stock
        """
        try:
            stock_code = lines[0][0]
            for line in lines:  # get every line's data
                if line[0] != stock_code:
                    raise RuntimeError("invalid format!")
                if line[1] == 'DA':
                    date = line[2]
                elif line[1] == 'OP':
                    opening_price = line[2]
                elif line[1] == 'HI':
                    high_price = line[2]
                elif line[1] == 'LO':
                    low_price = line[2]
                elif line[1] == 'CL':
                    closing_price = line[2]
                elif line[1] == 'VO':
                    volume = line[2]

            trading_data = stocks.TradingData(date, float(opening_price), float(high_price),
                                              float(low_price), float(closing_price), int(volume))
        except Exception as e:
            raise RuntimeError("invalid format!")
        stock = self._stocks.get_stock(stock_code)
        stock.add_day_data(trading_data)

    def _process(self, file):
        d = deque(maxlen=6)  # create a queue of 6 max length
        for i, line in enumerate(file):
            row = line.strip().split(':')
            d.append(row)
            if (i + 1) % 6 == 0:
                self._add_stock(d)


class HighLow(stocks.Analyser):
    """
    determines the highest and lowest prices paid for
    a stock across all of the data stored for the stock.
    """

    def __init__(self):
        self._high = 0.0
        self._low = float('inf')  # get a infinity number 

    def process(self, day):
        if day.get_high() > self._high:
            self._high = day.get_high()
        if day.get_low() < self._low:
            self._low = day.get_low()

    def reset(self):
        self._high = 0.0
        self._low = float('inf')

    def result(self):
        return self._high, self._low


class MovingAverage(stocks.Analyser):
    """
    calculates the average closing price of a stock over a specified period of time.
    """

    def __init__(self, num_days):
        self._num_days = num_days
        self._d = deque(maxlen=num_days)  # use a queue of num_days max length to store data

    def process(self, day):
        self._d.append(day.get_close())

    def reset(self):
        self._d.clear()

    def result(self):
        return sum(self._d) / self._num_days


class GapUp(stocks.Analyser):
    """
    finds the most recent day in the trading data where the stock’s opening price was
    significantly higher than its previous day’s closing price.
    """

    def __init__(self, delta):
        self._delta = delta
        self._last_day = None  # last day trading data
        self._gapup_day = None

    def process(self, day):
        if not self._last_day:
            self._last_day = day
        else:
            delta = day.get_open() - self._last_day.get_close()
            if delta > self._delta:
                self._gapup_day = day
            self._last_day = day

    def reset(self):
        self._last_day = None
        self._gapup_day = None

    def result(self):
        return self._gapup_day


def example_usage () :
    all_stocks = stocks.StockCollection()
    LoadCSV("march1.csv", all_stocks)
    LoadCSV("march2.csv", all_stocks)
    LoadCSV("march3.csv", all_stocks)
    LoadCSV("march4.csv", all_stocks)
    LoadCSV("march5.csv", all_stocks)
    LoadTriplet("feb1.trp", all_stocks)
    LoadTriplet("feb2.trp", all_stocks)
    LoadTriplet("feb3.trp", all_stocks)
    LoadTriplet("feb4.trp", all_stocks)
    volume = stocks.AverageVolume()
    stock = all_stocks.get_stock("ADV")
    stock.analyse(volume)
    print("Average Volume of ADV is", volume.result())
    high_low = HighLow()
    stock.analyse(high_low)
    print("Highest & Lowest trading price of ADV is", high_low.result())
    moving_average = MovingAverage(10)
    stock.analyse(moving_average)
    print("Moving average of ADV over last 10 days is {0:.2f}"
          .format(moving_average.result()))
    gap_up = GapUp(0.011)
    stock = all_stocks.get_stock("YOW")
    stock.analyse(gap_up)
    print("Last gap up date of YOW is", gap_up.result().get_date())


if __name__ == "__main__":
    example_usage()
