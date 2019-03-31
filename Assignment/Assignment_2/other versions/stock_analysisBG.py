import stocks


class LoadCSV(stocks.Loader):


    def _process(self, file):
        for line in file.readlines():
            line = line.strip('\r\n')
            items = line.split(',')
            print(items)
            code = items.pop(0)
            data = stocks.TradingData(items[0], float(items[1]), float(items[2]), float(items[3]), float(items[4]),
                                      int(items[5]))
            stock = stocks.Stock(code)
            stock.add_day_data(data)
            self._stocks.set_stock(code, stock)


class LoadTriplet(stocks.Loader):
    def __init__(self, filename, stocks):
        """Data is loaded on object creation.

        Parameters:
            filename (str): Name of the file from which to load data.
            stocks (StockCollection): Collection of existing stock market data
                                      to which the new data will be added.
        """
        # Maintain a reference to the stock colletion into which data is loaded.
        self._stocks = stocks
        with open(filename, "r") as file:
            # Use format specific subclass to parse the data in the file.
            self._process(file)

    def _process(self, file):
        data = file.readlines()
        group = len(data) // 6
        # sub the list about data read
        for x in range(group):
            open = x * 6
            end = open + 6
            temp = []
            code = '-1'
            for line in data[open:end]:
                line = line.strip('\r\n')
                items = line.split(':')
                code = items[0]
                temp.append(items[2])
            tradingData = stocks.TradingData(temp[0], float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]),
                                             int(temp[5]))
            stock = stocks.Stock(code)
            stock.add_day_data(tradingData)
            self._stocks.set_stock(code, stock)


if __name__ == "__main__":
    all_stocks = stocks.StockCollection()
    """LoadTriplet("data_files/feb1.trp", all_stocks)
    LoadTriplet("data_files/feb2.trp", all_stocks)
    LoadTriplet("data_files/feb3.trp", all_stocks)
    LoadTriplet("data_files/feb4.trp", all_stocks)"""
    LoadCSV("data_files/march1.csv", all_stocks)
    LoadCSV("data_files/march2.csv", all_stocks)
    LoadCSV("data_files/march3.csv", all_stocks)
    LoadCSV("data_files/march4.csv", all_stocks)
    LoadCSV("data_files/march5.csv", all_stocks)
    volume = stocks.AverageVolume()
    stock = all_stocks.get_stock("ADV")
    stock.analyse(volume)
    print("Average Volume of ADV is", volume.result())
