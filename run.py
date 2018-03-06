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

sys.path.insert(0, "/Users/ncpenke/code/pytaxes_forms")
sys.path.insert(0, getcwd())
sys.path.append(dirname(sys.argv[0]))

conf = importlib.import_module("conf")
forms = []
forms += conf.w2s

inputs = {}

tax_year = conf.tax_year

FilingStatus = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".form").FilingStatus
Form = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".form").Form
F8801 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".f8801").F8801
F1040 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".f1040").F1040
MNm1 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".mnm1").MNm1
CA540 = importlib.import_module("pytaxes_forms.y" + str(tax_year) + ".ca540").CA540

if conf.status == 'single':
    inputs['status'] = FilingStatus.SINGLE
elif conf.status == 'married_joint':
    inputs['status'] = FilingStatus.JOINT
elif conf.status == 'married_separate':
    inputs['status'] = FilingStatus.SEPARATE
elif conf.status == 'head':
    inputs['status'] = FilingStatus.HEAD
else:
    sys.exit("Unexpected filing status: " + conf.status)

for a in sys.argv[2:]:
    forms += importlib.import_module(a).forms

if len(conf.etrade_statements) > 0:
    forms += etrade.process_gains_and_losses(conf.etrade_statements)

if len(conf.etrade_holdings) > 0:
    if conf.simulate_etrade_sale_price >= 0:
        forms += simulate_etrade.simulate_sale_price(conf.etrade_holdings, conf.simulate_etrade_sale_price)[2]
    if conf.simulate_etrade_exercise_price >= 0:
        forms += simulate_etrade.simulate_exercise_price(conf.etrade_holdings, conf.simulate_etrade_sale_price)[2]

wages = 0
wages_state = 0
wages_ss = 0
wages_medicare = 0
withholding = 0
ss_withheld = 0
mediare_withheld = 0
capital_gain_long = conf.capital_gain_long_dist + conf.capital_gain_long
capital_gain_short = conf.capital_gain_short
qualified_dividends = conf.qualified_dividends
dividends = conf.dividends
total_proceeds = 0
stock_sale = False
amt_capital_gain_long = capital_gain_long
amt_iso_exercise = 0
state_withholding = 0
medicare_withheld = 0
group_life_insurance_taxable_costs = 0
retirement_401k_contribution = 0
hsa_employer_contribution = 0
employer_sponsered_health_coverage_cost = 0

for f in forms:
    if isinstance(f, StockSale):
        stock_sale = True
        total_proceeds += f.get('total_proceeds', 0.0)
        wages += f.get('ordinary_income', 0.0)
        capital_gain_short += f.get('capital_gain_short', 0.0)
        capital_gain_long += f.get('capital_gain_long', 0.0)
        amt_capital_gain_long += f.get('amt_capital_gain_long', f.get('capital_gain_long', 0.0))
    elif isinstance(f, StockExerciseISO):
        amt_iso_exercise += f.get('amt_iso_exercise', 0.0)
    else:
        t = f.get('type')
        if t  == 'w2':
            wages += f.get('1')
            wages_state += f.get('16')
            total_proceeds += f.get('1')
            withholding += f.get('2')
            wages_ss += f.get('3')
            ss_withheld += f.get('4')
            wages_medicare += f.get('5')
            medicare_withheld += f.get('6')
            state_withholding += f.get('17')
            codes = f.get('12')
            if isinstance(codes, dict):
                group_life_insurance_taxable_costs = codes.get('C')
                retirement_401k_contribution = codes.get('D')
                hsa_employer_contribution = codes.get('W')
                employer_sponsered_health_coverage_cost = codes.get('DD')
                
if inputs['status'] == FilingStatus.JOINT:
    inputs['wages'] = [wages, 0.0]
    inputs['wages_state'] = [wages_state, 0.0]
    inputs['withholding'] = withholding
    inputs['wages_ss'] = [wages_ss, 0.0]
    inputs['ss_withheld'] = [ss_withheld, 0.0]
    inputs['wages_medicare'] = [wages_medicare, 0.0]
    inputs['medicare_withheld'] = [medicare_withheld, 0.0]
else:
    inputs['wages'] = wages
    inputs['wages_state'] = wages_state
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
inputs['prior_amt_credit'] = conf.prior_amt_credit
inputs['prior_state_amt_credit'] = conf.prior_state_amt_credit
inputs['qualifying_children'] = conf.qualifying_children
inputs['exemptions'] = conf.exemptions
inputs['estimated_state_tax_payments'] = conf.estimated_state_tax_payments
inputs['extra_estimated_state_tax_payments'] = conf.extra_estimated_state_tax_payments
inputs['qualified_dividends'] = qualified_dividends
inputs['dividends'] = dividends
inputs['retirement_401k_contribution'] = retirement_401k_contribution
inputs['group_life_insurance_taxable_costs'] = group_life_insurance_taxable_costs
inputs['hsa_employer_contribution'] = hsa_employer_contribution
inputs['employer_sponsered_health_coverage_cost'] = employer_sponsered_health_coverage_cost

inputs['F1040sa'] = { '16' : conf.donations }
inputs['prev_F6251'] = Form({'Form' : conf.pf6251 })

f = F1040(inputs)
f.printAllForms()

sowed = 0
stax = 0

if conf.state == 'MN':
    s = MNm1(inputs, f)
    sowed = s['30']
    stax = s['9']
elif conf.state == 'CA':
    s = CA540(inputs, f)
    sowed = s['111']
    stax = s['64']
else:
    sys.exit("Unsupported state: " + conf.state)

s.printAllForms()

print("Total Income: %.2f" % total_proceeds)
fowed = f['78']
ftax = f['47']
agi = f['37']

print("AGI: %0.2f" % agi)
print("Total Tax: %0.2f" % (ftax + stax))
print("Federal Tax Owed: %0.2f" % fowed)
print("State Tax Owed: %0.2f" % sowed)
print("Total tax owed: %0.2f" % (fowed + sowed))

print("Post tax owed: %0.2f" % (total_proceeds - (fowed + sowed)))

for f in f.forms:
    if isinstance(f, F8801):
        print("AMT credit carryforward: %0.2f" % f['26'])

print("Effective federal tax rate: %.2f%%" % ((ftax / float(agi)) * 100))
print("Effective state tax rate: %.2f%%" % ((stax / float(agi)) * 100))
    
          
