# Wrapper around an excel sheet to easily allow accessing a column
# value by column name
class Sheet:
    def __init__(self, sheet):
        # Assume first row contains col names
        colNames = sheet[0]
        self.colNameToIdx = {}
        idx = 0
        for n in colNames:
            if n in self.colNameToIdx:
                p = self.colNameToIdx[n]
                if isinstance(p, list):
                    p.append(idx)
                else:
                    self.colNameToIdx[n] = [p, idx]
            else:
                self.colNameToIdx[n] = idx
            idx += 1
        self.rows = sheet[1:]
    def rowVal(self, row, colName):
        t = self.colNameToIdx[colName]
        if isinstance(t, list):
            ret = []
            for i in self.colNameToIdx[colName]:
                if i < len(row):
                    ret.append(row[i])
                else:
                    ret.append(None)
            return ret
        if t < len(row):
            return row[t]
        else:
            return None

        
