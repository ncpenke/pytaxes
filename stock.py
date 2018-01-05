class StockSale(dict):
    def __init__(self, sellPrice, count, gains, shortTerm):
        if shortTerm:
            self['capital_gain_short'] = gains
        else:
            self['capital_gain_long'] = gains
        self['total_proceeds'] = sellPrice * count

class StockSaleRSU(StockSale):
    def __init__(self, vestPrice, sellPrice, count, shortTerm):
        gains = (sellPrice - vestPrice) * count
        StockSale.__init__(self, sellPrice, count, gains, shortTerm)

class StockSaleISO(StockSale):
    # TODO: disqualified ISO sales
    def __init__(self, grantPrice, exercisePrice, sellPrice, count):
        gains = (sellPrice - grantPrice) * count
        StockSale.__init__(self, sellPrice, count, gains, False)
        self['amt_capital_gain_long'] = (sellPrice - exercisePrice) * count

class StockSaleESPP(StockSale):
    # TODO: disqualified ESPP sales
    def __init__(self, purchasePrice, discount, sellPrice, count):
        gains = (sellPrice - purchasePrice - discount) * count
        StockSale.__init__(self, sellPrice, count, gains, False)
        self['ordinary_income'] = discount * count

class StockExerciseISO(dict):
    def __init__(self, exercisePrice, grantPrice, count):
        self['amt_iso_exercise'] = (exercisePrice - grantPrice) * count
