"""
    __author__ = Jiabo Qin
    student number = 44273022
    __email__ = s4427302@uq.edu.au
"""

import stocks
from collections import deque #list-like container with fast appends and pops on either end from stardard library

class LoadCSV(stocks.Loader):
    """Load the data from CSV files."""
    def _process(self, file):
        """Load and parse the stock market data from 'file'."""
        try:
            for line in file:
                line = line.strip()
                items = line.split(',')
                stock_code = items[0]
                stock = self._stocks.get_stock(stock_code)
                data = stocks.TradingData(items[1],float(items[2]),float(items[3]),float(items[4]),float(items[5]),int(items[6]))
                stock.add_day_data(data)
        except Exception as e:
            raise RuntimeError()

class LoadTriplet(stocks.Loader):
    """Load the data from Triplet files."""
    def _process(self, file):
        """Load and parse the stock market data from 'file'."""
        data_list = deque(maxlen=6)  # create a queue of 6 max length
        for i, line in enumerate(file):
            data = line.strip().split(':')
            data_list.append(data)
            if (i + 1) % 6 == 0:
                self.add_stock(data_list)
                
    def add_stock(self, data_list):
        """
        Get data list information and create new Stock adding in stock_collection

        Parameters:
            data_list: Load and parse the stock market data from function _process.
        """
        try:
            stock_code = data_list[0][0]
            for line in data_list:  # get every list's data
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
        
class HighLow(stocks.Analyser):
    """determines the highest and lowest prices paid for a stock
        across all of the data stored for the stock.
    """
    
    def __init__(self):
        self._highest = 0.0
        self._lowest = float("inf")

    def process(self, value):
        """Comparing and collecting the highest and lowest prices
            across all of the data.

        Parameters:
            value (TradingData): Trading data for one stock across
            all of the data.
        """
        if value.get_high() > self._highest:
            self._highest = value.get_high()
        if value.get_low() < self._lowest:
            self._lowest = value.get_low()

    def reset(self) :
        """Reset the analysis process in order to perform a new analysis."""
        self._highest = 0.0
        self._lowest = float("inf")

    def result(self):
        """Return the highest and lowest prices for the processed stock.

        Return:
            float: The volume highest and lowest prices.
        """
        return (self._highest, self._lowest)

class MovingAverage(stocks.Analyser):
    """Calculates the average closing price of a stock
        over a specified period of time.
    """
    def __init__(self, num_days) :
        """
        Parameters:
            num_days(int): the number of last few days.
        """
        self._num_days = num_days
        self._value = deque(maxlen=num_days)
        self._sum_price = 0
        
    def process(self, day) :
        """Collect the closing price of the last number of days
            and sum them.

        Parameters:
            day(TradingData): Trading data for one stock on one day.
        """
        self._value.append(day.get_close())        

    def reset(self) :
        """Reset the analysis process in order to perform a new analysis."""
        self._value.clear()
        
    def result(self) :
        """
        Summing the all closing prices
        
        Return the average closing price of the last number of days.
        
        Return:
            float: Average closing price across a period time.
        """
        for each_price in self._value:
            self._sum_price += each_price
        return self._sum_price / self._num_days

class GapUp(stocks.Analyser):
    """find the most recent day in the trading data where the stock’s
        opening price was significantly higher than its previous day’s
        closing price."""
    
    def __init__(self, delta):
        """
        Parameters:
            delta(float): it is used to determine if the price difference is significant or not.
        """
        self._delta = delta
        self._last_day = None
        self._day = None
        
    def process(self, day):
        """Collect the opening price and the last day's closing price.
            Find the significant gap.

        Parameters:
            day(TradingData): Trading data for one stock on one day.
        """
        if self._last_day is None:
            self._last_day = day
        else:
            gap = day.get_open() - self._last_day.get_close()
            if gap > self._delta:
                self._day = day#date
            self._last_day = day#next step

    def reset(self) :
        """Reset the analysis process in order to perform a new analysis."""
        self._last_day = None
        self._day = None
        
    def result(self):
        """Return the date which has the significant gap.

        Return:
            float: the date which has the significant gap.
        """
        return self._day
        

def example_usage () :
    # Set up stock market    
    all_stocks = stocks.StockCollection()

    #loading in data
    LoadCSV("data_files/march1.csv", all_stocks)
    LoadCSV("data_files/march2.csv", all_stocks)
    LoadCSV("data_files/march3.csv", all_stocks)
    LoadCSV("data_files/march4.csv", all_stocks)
    LoadCSV("data_files/march5.csv", all_stocks)
    LoadTriplet("data_files/feb1.trp", all_stocks)
    LoadTriplet("data_files/feb2.trp", all_stocks)
    LoadTriplet("data_files/feb3.trp", all_stocks)
    LoadTriplet("data_files/feb4.trp", all_stocks)

    #example of a class that analyzers stock
    volume = stocks.AverageVolume()
    stock = all_stocks.get_stock("ADV")#All stuff below is gonna analyse ADV
    stock.analyse(volume)
    print("Average Volume of ADV is", volume.result())

    #testing HighLow Class
    high_low = HighLow()
    stock.analyse(high_low)
    print("Highest & Lowest trading price of ADV is", high_low.result())

    #testing MovingAverage Class
    moving_average = MovingAverage(10)
    stock.analyse(moving_average)
    print("Moving average of ADV over last 10 days is {0:.2f}"
          .format(moving_average.result()))

    #testing GapUp class
    gap_up = GapUp(0.011)
    stock = all_stocks.get_stock("YOW")
    stock.analyse(gap_up)
    print("Last gap up date of YOW is", gap_up.result().get_date())


if __name__ == "__main__" :
    example_usage()

