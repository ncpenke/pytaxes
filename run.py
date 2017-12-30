#!/usr/bin/env python
#
# Processes tax documents (W2s, stock sales, etc) encoded as python
# scripts and reports the tax for the year. 
#
# The first argument should be the configuration script which defines
# the filing status, resident state, previous year carryovers, etc.
# The subsequent arguments should be the tax documents. In the future
# documents (w2s, brokerage statements, etc) can be prcoessed directly
# but for now they need to be converted into a python script
#

import sys
import importlib
from os import getcwd
from os.path import dirname
from stock import *
import etrade

def usage():
    print('Usage: %s configuration tax-documents' % sys.argv[0])

if len(sys.argv) < 3:
    usage()
    sys.exit(1)

sys.path.append(dirname(sys.argv[0]))
sys.path.append(getcwd())

inputs = importlib.import_module(sys.argv[1]).conf
forms = []

for a in sys.argv[2:]:
    if a == "etrade.xlsx":
        forms += etrade.process_gains_and_losses(a)
    else:
        forms += importlib.import_module(a).forms

wages = 0
wages_ss = 0
wages_medicare = 0
withholding = 0
ss_withheld = 0
mediare_withheld = 0
capital_gain_long = inputs.get('capital_gain_long', 0)
capital_gain_short = inputs.get('capital_gain_short', 0)
capital_gain_dist = inputs.get('capital_gain_dist', 0)
amt_capital_gain_long = inputs.get('amt_capital_gain_long', 0)
state_withholding = 0
medicare_withheld = 0
tax_year = inputs.get('tax_year')

F1040 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".f1040").F1040
MNm1 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".mnm1").MNm1

for f in forms:
    if isinstance(f, StockSale):
        wages += f.get('ordinary_income', 0.0)
        capital_gain_short += f.get('capital_gain_short', 0.0)
        capital_gain_long += f.get('capital_gain_long', 0.0)
        amt_capital_gain_long += f.get('amt_capital_gain_long', f.get('capital_gain_long', 0.0))
    else:
        t = f.get('type')
        if t  == 'w2':
            wages += f.get('1')
            withholding += f.get('2')
            wages_ss += f.get('3')
            ss_withheld += f.get('4')
            wages_medicare += f.get('5')
            medicare_withheld += f.get('6')
            state_withholding += f.get('17')

inputs['wages'] = [wages, 0.0]
inputs['withholding'] = withholding
inputs['wages_ss'] = [wages_ss, 0.0]
inputs['ss_withheld'] = [ss_withheld, 0.0]
inputs['wages_medicare'] = [wages_medicare, 0.0]
inputs['medicare_withheld'] = [medicare_withheld, 0.0]
inputs['state_withholding'] = state_withholding
inputs['capital_gain_long'] = capital_gain_long
inputs['capital_gain_short'] = capital_gain_short
inputs['amt_capital_gain_long'] = amt_capital_gain_long

f = F1040(inputs)
f.printAllForms()

if inputs['state'] == 'MN':
    m = MNm1(inputs, f)
    m.printAllForms()
