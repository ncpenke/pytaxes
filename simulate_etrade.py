import pyexcel_xlsx
import sys
from sheet import *
from stock import *

total = 0
totalExercise = 0
totalShares = 0
totalExerciseShares = 0

def strip_dollar(s):
    if len(s) == 0:
        return 0
    if s[0] == '$':
        return float(s[1:])
    return float(s)

def percent_to_dec(s):
    if len(s) == 0:
        return 0
    if s[len(s) - 1] == '%':
        return float(s[0:len(s) - 1]) / 100

def process_sale(filename, sellPrice):
    d = pyexcel_xlsx.get_data(filename)
    espp = d['ESPP']
    rsu = d['Restricted Stock']
    iso = d['Options']
    r = process_espp(espp, sellPrice)
    r += process_rsu(rsu, sellPrice)
    r += process_iso(iso, sellPrice)
    return r

def process_exercise(filename, exercisePrice):
    d = pyexcel_xlsx.get_data(filename)
    options = d['Options']
    return process_exercise_options(options, exercisePrice)

def process_espp(espp, sellPrice):
    total = 0
    totalShares = 0
    espp = Sheet(espp)
    nespp = 0
    forms = []
    for row in espp.rows:
        t = espp.rowVal(row, 'Record Type')
        if t == 'Purchase':
            low = min(strip_dollar(espp.rowVal(row, 'Grant Date FMV')),
                      strip_dollar(espp.rowVal(row, 'Purchase Date FMV')))
            discount = low * percent_to_dec(espp.rowVal(row, 'Discount Percent'))
            purchasePrice = low - discount
            n = float(espp.rowVal(row, 'Sellable Qty.'))
            d = espp.rowVal(row, 'Purchase Date')
            if '2017' not in d:
                forms.append(StockSaleESPP(purchasePrice, discount, sellPrice, n, False))
                total += sellPrice * n
                totalShares += n
                nespp += n
    print("Num ESPP: %s" % nespp)
    return [ total, totalShares, forms ]

def process_rsu(rsu, sellPrice):
    total = 0
    totalShares = 0
    forms = []
    rsu = Sheet(rsu)
    nrsu = 0
    for row in rsu.rows:
        t = rsu.rowVal(row, 'Record Type')
        if t == 'Sellable Shares':
            n = rsu.rowVal(row, 'Sellable Qty.')[2]
            basis = float(rsu.rowVal(row, 'Est. Cost Basis (per share):'))
            taxStatus = rsu.rowVal(row, 'Tax Status SL')
            if taxStatus == 'Long Term':
                forms.append(StockSaleRSU(basis, sellPrice, n, False))
                total += sellPrice * n
                totalShares += n
                nrsu += n
    print("Num RSU: %s" % nrsu)
    return [ total, totalShares, forms ]

def process_iso(iso, sellPrice):
    total = 0
    totalShares = 0
    forms = []
    iso = Sheet(iso)
    niso = 0
    for row in iso.rows:
        t = iso.rowVal(row, 'Record Type')
        if (t == 'Sellable Shares'):
            exercisePrice = float(iso.rowVal(row, 'Exercise Price'))
            n = float(iso.rowVal(row, 'Sellable Qty.')[1])
            grantPrice = float(iso.rowVal(row, 'Est. Cost Basis (per share):'))
            forms.append(StockSaleISO(grantPrice, exercisePrice, sellPrice, n, True))
            total += sellPrice * n
            totalShares += n
            niso += n
    print("Num ISO: %s" % niso)
    return [ total, totalShares, forms ]

def process_exercise_options(options, exercisePrice):
    total = 0
    totalShares = 0
    forms = []
    options = Sheet(options)
    nisos = 0
    nnqos = 0
    for row in options.rows:
        t = options.rowVal(row, 'Record Type')
        if (t == 'Grant'):
            grantPrice = float(options.rowVal(row, 'Exercise Price'))
            n = float(options.rowVal(row, 'Exercisable Qty.')[0])
            forms.append(StockExerciseISO(exercisePrice, grantPrice, n))
            total += exercisePrice * n
            totalShares += n
            noptions += n
    print("Num exercised ISO: %s" % nisos)
    print("Num exercised NQO: %s" % nnqos)
    return [ total, totalShares, forms ]

def simulate_sale_price(filename, sellPrice):
    r = process_sale(filename, sellPrice)
    print ("Total: %s %s" % (r[0], r[1]))
    return r

def simulate_exercise_price(filename, exercisePrice):
    r = process_exercise(filename, exercisePrice)
    print ("Total: %s %s" % (r[0], r[1]))
    return r


