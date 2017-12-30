# Wrapper around an excel sheet to easily allow accessing a column
# value by column name
class Sheet:
    def __init__(self, sheet):
        # Assume first row contains col names
        colNames = sheet[0]
        self.colNameToIdx = {}
        idx = 0
        for n in colNames:
            self.colNameToIdx[n] = idx
            idx += 1
        self.rows = sheet[1:]
    def rowVal(self, row, colName):
        return row[self.colNameToIdx[colName]]

        
