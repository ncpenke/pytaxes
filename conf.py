# This is the configuration file for the tax estimator. Copy this file
# to another directory and fill in your details.

################################################################
#
# Personal Info
#
################################################################

# Year for which taxes are being estimated: 2017 or 2018
tax_year = 2018

# Your filing status:
#
# single: filing as single
# married_joint: married and filing jointly
# married_separate: married and filing separately
# head: filing as head of household
status = "single"

# Number of dependants you're claiming
exemptions = 0

# Number of children that qualify for the child tax credit
qualifying_children = 0

# Resident state: CA or MN
state = 'MN'

################################################################
#
# Estimated Payments
#
################################################################

# Estimated payments for federal taxes
estimated_payments = 0

# State tax payments that were made on or before december 31st of the
# tax year. Ex: If you're estimating taxes for 2017 then include the
# state tax payments that were made on or before December 31, 2017. Do
# NOT include any 2017 state tax payments that were made in 2018.
estimated_state_tax_payments = 0

# State tax payments that were made after the tax year year for the
# tax year. Ex. state taxes for 2017 that were paid on March, 2018.
extra_estimated_state_tax_payments = 0

################################################################
#
# etrade employee stock plan
#
################################################################
#
# Modify the variable below to point to the path of the exported trade
# confirmations.
#
# To export trade confirmations:
#
#  1. Log into etrade and select your employee stock plan
#
#  2. Hover over "My Account" and select "Gains & Losses" from the drop down
#
#  3. Select the appropriate tax year
#
#  4. Select "Download" followed by "Download Expanded" in the drop
#     down. Save the file in the same directory as your configuration
#     file.
#
#  5. Modify below with the filename
etrade_statements = '' # 'etrade_statements.xlsx'

# To estimate taxes on hypothetical stock trades in etrade, first
# export all your etrade holdings:
#
#  1. Log onto etrade and navigate to the appropriate brokerage
#     accounts
#
#  2. Select the "Holdings" tab
#
#  3. Select the "Download" dropdown and select "Download Expanded"
#
#  4. Save the file in the same directory as your configuration file
#
#  5. Modify below with the filename
etrade_holdings = '' # 'ByBenefitType.xlsx'

# If you have any stock options that need to be exercised, indicate the
# exercise price you would like to simulate.
simulate_etrade_exercise_price = -1

# Simulate the sale price of any stock that needs to be sold
simulate_etrade_sale_price = -1

################################################################
#
# W2s
#
################################################################

w2s = []

# Fill in your w2s
w2 = {}
w2['type'] = 'w2'
w2['1'] = 0
w2['2'] = 0
w2['3'] = 0
w2['4'] = 0
w2['5'] = 0
w2['6'] = 0
w2['12'] = {}
# Add remove other codes as needed here
w2['12']['C'] = 0
w2['12']['D'] = 0
w2['12']['DD'] = 0
w2['12']['W'] = 0
w2['16'] = 0
w2['17'] = 0
w2s.append(w2)

# Repeat as needed for more w2s

################################################################
#
# Dividends, distributions, and capital gains
#
################################################################

# Total ordinary dividends. Taxed as ordinary income.
dividends = 0

# Total qualified dividends. Taxed as capital gains.
qualified_dividends = 0

# Total long-term capital gain distributions. Taxed as capital gains.
capital_gain_long_dist = 0

# Total long-term capital gain. If you exported statements from
# etrade, then do not include any capital gains from etrade here.
capital_gain_long = 0

# Total short-term capital gains. If you exported statements from
# etrade, then do not include any capital gains due to etrade here
capital_gain_short = 0

################################################################
#
# Donations
#
################################################################

# Total amount donated.
donations = 0

################################################################
#
# Prior year's tax information
#
################################################################

# AMT credit that's carried forward from previous years (see form 8801
# from previous year's filing)
prior_amt_credit = 0

# AMT credit for your that's carried forward from previous years (this
# is only applicable to states that have the AMT like CA).
prior_state_amt_credit = 0

# Passive activity loss carried over from the previous year (these are
# losses from passive income such as income generated from an
# investment property)
prior_passive_activity_loss = 0

# Fill in values from the previous year's federal 6251 (this can be
# found in your previous year's tax return).
pf6251 = {}
pf6251['1'] = 0
pf6251['3'] = 0
pf6251['5'] = 0
pf6251['6'] = 0
pf6251['7'] = 0
pf6251['11'] = 0
pf6251['12'] = 0
pf6251['13'] = 0
pf6251['14'] = 0
pf6251['17'] = 0
pf6251['19'] = 0
pf6251['28'] = 0
pf6251['34'] = 0
pf6251['35'] = 0



