# https://medium.com/analytics-vidhya/building-an-intrinsic-value-calculator-with-python-7986833962cd
# https://medium.com/swlh/automating-your-stock-portfolio-research-with-python-for-beginners-912dc02bf1c2
# Derek - 30 Nov 2020 after learning the youtUbe GIT toturial
# after dinner
# after working on the Excel spreadsheet

import requests
import pandas as pd
import openpyxl

gmail_key = 'd50a1da239d59fb8401cba97e42c046e'
wlan04_key = 'b78085543053f2fc69099f1c23179c82'

apiKey1 = gmail_key

# https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=d50a1da239d59fb8401cba97e42c046e

def getdata(stock):
    # Company Quote Group of Items
    # company_quote = requests.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey=d50a1da239d59fb8401cba97e42c046e")
    company_quote = requests.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={apiKey1}")
    company_quote = company_quote.json()
    # return is a List of Dictionary
    print(company_quote)
    share_price = float("{0:.2f}".format(company_quote[0]['price']))

    # Balance Sheet Group of Items
    # https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/AAPL?apikey=d50a1da239d59fb8401cba97e42c046e&period=quarter
    # BS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{stock}?apikey=d50a1da239d59fb8401cba97e42c046e&period=quarter")
    BS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{stock}?apikey={apiKey1}")
    BS = BS.json()

    # Total Debt
    debt = float("{0:.2f}".format(float(BS['financials'][0]['Total debt']) / 10 ** 9))  # Total Cash
    cash = float("{0:.2f}".format(float(BS['financials'][0]['Cash and short-term investments']) / 10 ** 9))

    # Income Statement Group of Items
    # IS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}?period=quarter&apikey=d50a1da239d59fb8401cba97e42c046e")
    IS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}?period=quarter&apikey={apiKey1}")
    IS = IS.json()

    # Most Recent Quarterly Revenue
    qRev = float("{0:.2f}".format(float(IS['financials'][0]['Revenue']) / 10 ** 9))

    # Company Profile Group of Items
    # company_info = requests.get(f"https://financialmodelingprep.com/api/v3/company/profile/{stock}?apikey=d50a1da239d59fb8401cba97e42c046e")
    company_info = requests.get(
        f"https://financialmodelingprep.com/api/v3/company/profile/{stock}?apikey={apiKey1}")
    company_info = company_info.json()
    # Chief Executive Officer
    ceo = company_info['profile']['ceo']

    return (share_price, cash, debt, qRev, ceo)


tickers = ('AAPL', 'MSFT')

data = map(getdata, tickers)
dataList = list(map(getdata,tickers))
for i in dataList:
  print(i)

df = pd.DataFrame(data, columns=['Stock Price', 'Total Cash', 'Total Debt', 'Q3 2019 Revenue', 'CEO'], index=tickers)

print(df)

# Writing to Excel
writer = pd.ExcelWriter('example.xlsx')
df.to_excel(writer, 'Statistics')
writer.save()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
