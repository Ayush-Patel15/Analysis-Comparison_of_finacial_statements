## IMPORTS
from db_connect import connect_to_the_database, insert_and_update_collection
from scraper import scrape_stocklist_from_indices, scrape_income_statement_stock, scrape_balance_sheet_stock
import numpy as np
from matplotlib.pyplot import Figure
from io import BytesIO
import base64
import time

## GLOBAL VARIABLES
NIFTY50_URL = "https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"
INCOME_STATEMENT_URL = "https://www.moneycontrol.com/financials/{0}/consolidated-profit-lossVI/{1}/{2}"
INCOME_STATEMENT_STANDALONE_URL = "https://www.moneycontrol.com/financials/{0}/profit-lossVI/{1}/{2}"
BALANCE_SHEET_URL = "https://www.moneycontrol.com/financials/{0}/consolidated-balance-sheetVI/{1}/{2}"
BALANCE_SHEET_STANDALONE_URL = "https://www.moneycontrol.com/financials/{0}/balance-sheetVI/{1}/{2}"

# function to insert the list of nifty 50 stocks
def insert_nifty50_stocklist():
    nifty_stocks = scrape_stocklist_from_indices(indices_url=NIFTY50_URL)
    db = connect_to_the_database(database="Fundamentals")
    for stock in nifty_stocks:
        print(insert_and_update_collection(db, "nifty_list", "code", stock))
    return nifty_stocks

# function to insert the income statement of all nifty 50 stocks
def insert_income_statements_stocks():
    db = connect_to_the_database(database="Fundamentals")
    all_stocks = list(db["nifty_list"].find({}))
    for stock in all_stocks:
        print(stock)
        time.sleep(5)
        income_statement_data = {}
        income_statement_data["full_name"] = stock["full_name"]
        income_statement_data["url_name"] = stock["url_name"]
        income_statement_data["code"] = stock["code"]
        try:
            scraped_data = scrape_income_statement_stock(
                INCOME_STATEMENT_URL.format(stock["url_name"], stock["code"], "1"),
                INCOME_STATEMENT_URL.format(stock["url_name"], stock["code"], "2"),
            )
        except Exception as e:
            scraped_data = scrape_income_statement_stock(
                INCOME_STATEMENT_STANDALONE_URL.format(stock["url_name"], stock["code"], "1"),
                INCOME_STATEMENT_STANDALONE_URL.format(stock["url_name"], stock["code"], "2")
            )
        income_statement_data["data"] = scraped_data
        print(insert_and_update_collection(db, "income_statements", "code", income_statement_data))
    return "msg: All 50 stocks inserted successfully..!"

# function to insert the balance sheet of all nifty 50 stocks
def insert_balance_sheet_stocks():
    db = connect_to_the_database(database="Fundamentals")
    all_stocks = list(db["nifty_list"].find({}))
    for stock in all_stocks:
        print(stock)
        time.sleep(5)
        balance_sheet_data = {}
        balance_sheet_data["full_name"] = stock["full_name"]
        balance_sheet_data["url_name"] = stock["url_name"]
        balance_sheet_data["code"] = stock["code"]
        try:
            scraped_data = scrape_balance_sheet_stock(
                BALANCE_SHEET_URL.format(stock["url_name"], stock["code"], "1"),
                BALANCE_SHEET_URL.format(stock["url_name"], stock["code"], "2")
            )
        except Exception as e:
            scraped_data = scrape_balance_sheet_stock(
                BALANCE_SHEET_STANDALONE_URL.format(stock["url_name"], stock["code"], "1"),
                BALANCE_SHEET_STANDALONE_URL.format(stock["url_name"], stock["code"], "2")
            )
        balance_sheet_data["data"] = scraped_data
        print(insert_and_update_collection(db, "balance_sheets", "code", balance_sheet_data))
    return "msg: All 50 stocks inserted successfully..!"

# Base function to plot graph of any required section
def plot_graph(xAxis, yAxis, xLabel, yLabel):
    fig = Figure(facecolor="#FFD700")
    plt = fig.subplots()
    plt.plot(xAxis, yAxis, color="black")
    plt.set_xlabel(xLabel)
    plt.set_ylabel(yLabel)
    plt.set_xticks(xAxis[1::2])
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    image = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return image

# function to plot graph of working capital of a company
def plot_working_capital(balance_sheet_data):
    try:
        current_assets = np.array(balance_sheet_data["Total Current Assets"], dtype="f")
        current_liabilities = np.array(balance_sheet_data["Total Current Liabilities"], dtype="f")
        working_capital = current_assets - current_liabilities
    except Exception as e:
        current_assets = np.array(balance_sheet_data["Cash and Balances with Reserve Bank of India"], dtype="f") + \
                        np.array(balance_sheet_data["Balances with Banks Money at Call and Short Notice"], dtype="f") + \
                        np.array(balance_sheet_data["Other Assets"], dtype="f")
        current_liabilities = np.array(balance_sheet_data["Other Liabilities and Provisions"], dtype="f")
        working_capital = current_assets - current_liabilities
    years = balance_sheet_data["YEARS"][::-1]
    working_capital = working_capital[::-1]
    working_capital_graph = plot_graph(years, working_capital, "YEARS", "WORKING CAPITAL")
    return working_capital_graph

# function to plot graph of working capital of a company
def plot_current_ratio(balance_sheet_data):
    try:
        current_assets = np.array(balance_sheet_data["Total Current Assets"], dtype="f")
        current_liabilities = np.array(balance_sheet_data["Total Current Liabilities"], dtype="f")
        current_ratio = current_assets / current_liabilities
    except Exception as e:
        current_assets = np.array(balance_sheet_data["Cash and Balances with Reserve Bank of India"], dtype="f") + \
                        np.array(balance_sheet_data["Balances with Banks Money at Call and Short Notice"], dtype="f") + \
                        np.array(balance_sheet_data["Other Assets"], dtype="f")
        current_liabilities = np.array(balance_sheet_data["Other Liabilities and Provisions"], dtype="f")
        current_ratio = current_assets / current_liabilities
    years = balance_sheet_data["YEARS"][::-1]
    current_ratio = current_ratio[::-1]
    current_ratio_graph = plot_graph(years, current_ratio, "YEARS", "CURRENT RATIO")
    return current_ratio_graph

if __name__ == "__main__":
    # insert_nifty50_stocklist()
    # print(insert_income_statements_stocks())
    print(insert_balance_sheet_stocks())
