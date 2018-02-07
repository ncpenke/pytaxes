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
    def __init__(self, grantPrice, exercisePrice, sellPrice, count, disqualified):
        if disqualified:
            self['ordinary_income'] = (sellPrice - grantPrice) * count
            StockSale.__init__(self, sellPrice, count, 0, False)
        else:
            gains = (sellPrice - grantPrice) * count
            StockSale.__init__(self, sellPrice, count, gains, False)
            self['amt_capital_gain_long'] = (sellPrice - exercisePrice) * count

class StockSaleNQO(StockSale):
    def __init__(self, grantPrice, exercisePrice, sellPrice, count, shortTerm):
        gains = (sellPrice - exercisePrice) * count
        StockSale.__init__(self, sellPrice, count, gains, shortTerm)

class StockSaleESPP(StockSale):
    def __init__(self, purchasePrice, discount, sellPrice, count, disqualified):
        ordinaryIncome = discount * count
        gains = (sellPrice - purchasePrice - discount) * count
        if disqualified:
            ordinaryIncome += gains
            gains = 0
        StockSale.__init__(self, sellPrice, count, gains, False)
        assert(discount >= 0)
        assert(ordinaryIncome >= 0)
        self['ordinary_income'] = ordinaryIncome

class StockExerciseISO(dict):
    def __init__(self, exercisePrice, grantPrice, count):
        assert(exercisePrice > grantPrice)
        self['amt_iso_exercise'] = (exercisePrice - grantPrice) * count

class StockExerciseNQO(dict):
    def __init__(self, exercisePrice, grantPrice, count):
        assert(exercisePrice > grantPrice)
        self['ordinary_income'] = (exercisePrice - grantPrice) * count
                     
                    
