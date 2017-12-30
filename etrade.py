import pyexcel_xlsx
import json
import sys
from stock import *

# Process gains and losses exported from ETrade
class GLProcessor:
    def __init__(self, filename):
        data = pyexcel_xlsx.get_data(filename)
        sheet_names = data.keys()
        if len(sheet_names) != 1:
            raise RuntimeError("Expecting one sheet in " + filename)
        sheet = data[sheet_names[0]]
        colnames = sheet[0]

        self.namestoidx = {}
        self.sales = []

        idx = 0
        for col in colnames:
            self.namestoidx[col] = idx
            idx += 1

        for row in sheet[1:]:
            type = self.__get__(row, 'Plan Type')
            if (type == "RS"):
                self.sales.append(StockSaleRSU(self.__get__(row, "Ordinary Income Recognized Per Share"),
                                               self.__get__(row, "Proceeds Per Share"),
                                               self.__get__(row, "Qty."),
                                               self.__get__(row, "Term") == "Short"))
            elif (type == "SO"):
                self.sales.append(StockSaleISO(self.__get__(row, "Grant Price"),
                                               self.__get__(row, "Exercise Date FMV"),
                                               self.__get__(row, "Proceeds Per Share"),
                                               self.__get__(row, "Qty.")))
            elif (type == "ESPP"):
                self.sales.append(StockSaleESPP(self.__get__(row, "Acquisition Cost Per Share"),
                                                self.__get__(row, "Discount Amount"),
                                                self.__get__(row, "Proceeds Per Share"),
                                                self.__get__(row, "Qty.")))

    def __get__(self, row, name):
        s = row[self.namestoidx[name]]
        if type(s) is str and len(s) > 0 and s[0] == '$':
            s = s[1:]
        return s

def process_gains_and_losses(filename):
    return GLProcessor(filename).sales

if __name__ == "__main__":
    print json.dumps(process_gains_and_losses(sys.argv[1]))
 
        
