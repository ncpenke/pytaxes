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
import simulate_etrade

def usage():
    print('Usage: %s configuration tax-documents' % sys.argv[0])

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

sys.path.append(dirname(sys.argv[0]))
sys.path.append(getcwd())

inputs = importlib.import_module(sys.argv[1]).conf
forms = []

for a in sys.argv[2:]:
    forms += importlib.import_module(a).forms

if 'etrade' in inputs:
    forms += etrade.process_gains_and_losses(inputs['etrade'])

if 'simulate_etrade' in inputs:
    if 'simulate_sale_price' in inputs:
        forms += simulate_etrade.simulate_sale_price(inputs['simulate_etrade'], inputs['simulate_sale_price'])[2]
    if 'simulate_exercise_price' in inputs:
        forms += simulate_etrade.simulate_exercise_price(inputs['simulate_etrade'], inputs['simulate_exercise_price'])[2]

wages = 0
wages_ss = 0
wages_medicare = 0
withholding = 0
ss_withheld = 0
mediare_withheld = 0
capital_gain_long = inputs.get('capital_gain_long', 0)
capital_gain_short = inputs.get('capital_gain_short', 0)
capital_gain_dist = inputs.get('capital_gain_dist', 0)
total_proceeds = 0
amt_capital_gain_long = inputs.get('amt_capital_gain_long', 0)
amt_iso_exercise = inputs.get('amt_iso_exercise', 0)
state_withholding = 0
medicare_withheld = 0
tax_year = inputs.get('tax_year')

FilingStatus = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".form").FilingStatus
F8801 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".f8801").F8801
F1040 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".f1040").F1040
MNm1 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".mnm1").MNm1

for f in forms:
    if isinstance(f, StockSale):
        total_proceeds += f.get('total_proceeds', 0.0)
        wages += f.get('ordinary_income', 0.0)
        capital_gain_short += f.get('capital_gain_short', 0.0)
        capital_gain_long += f.get('capital_gain_long', 0.0)
        amt_capital_gain_long += f.get('amt_capital_gain_long', f.get('capital_gain_long', 0.0))
    if isinstance(f, StockExerciseISO):
        amt_iso_exercise += f.get('amt_iso_exercise', 0.0)
    else:
        t = f.get('type')
        if t  == 'w2':
            wages += f.get('1')
            total_proceeds += f.get('1')
            withholding += f.get('2')
            wages_ss += f.get('3')
            ss_withheld += f.get('4')
            wages_medicare += f.get('5')
            medicare_withheld += f.get('6')
            state_withholding += f.get('17')

if inputs['status'] == FilingStatus.JOINT:
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
    inputs['amt_iso_exercise'] = amt_iso_exercise
else:
    inputs['wages'] = wages
    inputs['withholding'] = withholding
    inputs['wages_ss'] = wages_ss
    inputs['ss_withheld'] = ss_withheld
    inputs['wages_medicare'] = wages_medicare
    inputs['medicare_withheld'] = medicare_withheld
    inputs['state_withholding'] = state_withholding
    inputs['capital_gain_long'] = capital_gain_long
    inputs['capital_gain_short'] = capital_gain_short
    inputs['amt_capital_gain_long'] = amt_capital_gain_long
    inputs['amt_iso_exercise'] = amt_iso_exercise

f = F1040(inputs)
f.printAllForms()

if inputs['state'] == 'MN':
    s = MNm1(inputs, f)
    s.printAllForms()

if total_proceeds > 0:
    print("Total: %s" % total_proceeds)
    fowed = f['78']
    ftax = f['47']
    sowed = s['30']
    stax = s['9']
    agi = f['37']

    print("AGI: %s" % agi)
    print("Tax owed: %s" % (ftax + stax))
    print("Post tax: %s" % (total_proceeds - (ftax + stax)))
    print("Post tax owed: %s" % (total_proceeds - (fowed + sowed)))

    for f in f.forms:
        if isinstance(f, F8801):
            print("AMT credit carryforward: %s" % f['26'])

    print("Effective federal tax rate: %.2f%%" % ((ftax / float(agi)) * 100))
    print("Effective state tax rate: %.2f%%" % ((stax / float(agi)) * 100))
    
          
