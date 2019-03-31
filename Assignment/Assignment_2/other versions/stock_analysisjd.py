import stocks






class LoadCSV(stocks.Loader) :

    def _process(self,file):

        try:
            for line in file :
                line = line.strip()
                item = line.split(",")
                stock_code = item[0]
                stock = self._stocks.get_stock(stock_code)
                trading_data = stocks.TradingData(item[1],float(item[2]),float(item[3]),float(item[4]),float(item[5]),float(item[6]))
                stock.add_day_data(trading_data)

        except IndexError :
            raise RuntimeError("invalid format")
    




class LoadTriplet(stocks.Loader):


  

    def _process(self, file):
        """Iterate through the file, extracting the data from a line"""        

        stocks_list = []
        try:
            for line in file:
                line = line.strip()
                stocks_list = line.split(":")
                code = stocks_list[0]
                if stocks_list[1] == "DA":
                    DA = stocks_list[2]
                elif stocks_list[1] == "OP":
                    OP = stocks_list[2]
                elif stocks_list[1] == "HI":
                    HI = stocks_list[2]
                elif stocks_list[1] == "LO":
                    LO = stocks_list[2]
                elif stocks_list[1] == "CL":
                    CL = stocks_list[2]
                elif stocks_list[1] == "VO":
                    VO = stocks_list[2]
                    trading_data = stocks.TradingData(DA, float(OP), float(HI), float(LO), float(CL), int(VO))
                    single_stock = self._stocks.get_stock(code)
                    single_stock.add_day_data(trading_data)
                     
        except IndexError:
            raise RuntimeError
        





class HighLow(stocks.Analyser):
 

    def __init__(self):
        self._high = 0
        self._low = float('inf')  

    def process(self, day):
        if day.get_high() > self._high:
            self._high = day.get_high()
        if day.get_low() < self._low:
            self._low = day.get_low()

    def reset(self):
        self._high = 0
        self._low = float('inf')

    def result(self):
        return self._high, self._low


class MovingAverage(stocks.Analyser):
   

    def __init__(self, num_days):
        self._num_days = num_days
        self._d = []
        

    def process(self, day):
        if len(self._d) < self._num_days:
            for i in range(self._num_days):
                self._d.append(day.get_close())
        del(self._d[0])
        self._d.append(day.get_close())        
 

    def reset(self):
        self._num_days = None
        self._close = None
        self._sums = 0

    def result(self):
        return sum(self._d) / self._num_days


class GapUp(stocks.Analyser):
 

    def __init__(self, delta):
        self._delta = delta
        self._last_day = None  
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



    
