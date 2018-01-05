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
    r = process_espp(espp)
    r += process_rsu(rsu)
    r += process_iso(iso)

def process_exercise(filename, exercisePrice):
    d = pyexcel_xlsx.get_data(filename)
    iso = d['Options']
    return process_exercise_iso(iso, exercisePrice)

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
                forms.append(StockSaleESPP(purchasePrice, discount, sellPrice, n))
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
            n = rsu.rowVal(row, 'Sellable Qty.')
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
            n = float(iso.rowVal(row, 'Sellable Qty.'))
            grantPrice = float(iso.rowVal(row, 'Est. Cost Basis (per share):'))
            forms.append(StockSaleISO(grantPrice, exercisePrice, sellPrice, n))
            total += sellPrice * n
            totalShares += n
            niso += n
    print("Num ISO: %s" % niso)
    return [ total, totalShares, forms ]

def process_exercise_iso(iso, exercisePrice):
    total = 0
    totalShares = 0
    forms = []
    iso = Sheet(iso)
    niso = 0
    for row in iso.rows:
        t = iso.rowVal(row, 'Record Type')
        if (t == 'Grant'):
            grantPrice = float(iso.rowVal(row, 'Exercise Price'))
            n = float(iso.rowVal(row, 'Exercisable Qty.')[0])
            forms.append(StockExerciseISO(exercisePrice, grantPrice, n))
            total += exercisePrice * n
            totalShares += n
            niso += n
    print("Num exercised ISO: %s" % niso)
    return [ total, totalShares, forms ]

def simulate_sale_price(filename, sellPrice):
    r = process_sale(filename, sellPrice)
    print ("Total: %s %s" % (r[0], r[1]))
    return r

def simulate_exercise_price(filename, exercisePrice):
    r = process_exercise(filename, exercisePrice)
    print ("Total: %s %s" % (r[0], r[1]))
    return r


