## IMPORTS
from db_connect import connect_to_the_database, insert_and_update_collection
from scraper import scrape_stocklist_from_indices, scrape_income_statement_stock, scrape_balance_sheet_stock
import numpy as np
from matplotlib.pyplot import Figure
from io import BytesIO
import base64
import time

## GLOBAL VARIABLES
## #FFD700: Golden like color
## #28282B: Black like color
## #F5F5F5: white like color
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
def plot_graph(xAxis, yAxis, xLabel, yLabel, graphType, threshold=0, facecolor="#FFD700"):
    fig = Figure(facecolor=facecolor)
    plt = fig.subplots()
    if graphType == "line":
        plt.plot(xAxis, yAxis, color="black", marker="o")
    elif graphType == "bar":
        plt.bar(xAxis, yAxis, color="black")
    plt.set_xlabel(xLabel)
    plt.set_ylabel(yLabel)
    plt.set_xticks(xAxis[1::2])
    # Horizontal threshold point
    plt.axhline(y=threshold, color="black", linestyle="dashed")
    # If facecolor is black
    if facecolor == "#28282B":  # black
        plt.xaxis.label.set_color("#F5F5F5")    # white
        plt.yaxis.label.set_color("#F5F5F5")
        plt.tick_params(colors="#F5F5F5", which='both')
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
    working_capital_graph = plot_graph(years, working_capital, "YEARS", "WORKING CAPITAL", "bar", 0)
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
    current_ratio_graph = plot_graph(years, current_ratio, "YEARS", "CURRENT RATIO", "line", 1)
    return current_ratio_graph

# function to plot graph of Return on Assets (ROA) of a company
def plot_return_on_assets(income_statement_data, balance_sheet_data):
    try:
        net_profit = np.array(income_statement_data["Profit/Loss For The Period"], dtype="f")
    except Exception as e:
        net_profit = np.array(income_statement_data["Net Profit / Loss for The Year"], dtype="f")
    total_assets = np.array(balance_sheet_data["Total Assets"], dtype="f")
    return_on_assets = (net_profit / total_assets) * 100
    years = income_statement_data["YEARS"][::-1]
    return_on_assets = return_on_assets[::-1]
    return_on_assets_graph = plot_graph(years, return_on_assets, "YEARS", "ROA (%)", "line", facecolor="#28282B")
    return return_on_assets_graph

# function to plot graph of Return on Equity (ROE) of a company
def plot_return_on_equity(income_statement_data, balance_sheet_data):
    try:
        net_profit = np.array(income_statement_data["Profit/Loss For The Period"], dtype="f")
        total_equity = np.array(balance_sheet_data["Total Shareholders Funds"], dtype="f")
    except Exception as e:
        net_profit = np.array(income_statement_data["Net Profit / Loss for The Year"], dtype="f")
        total_equity = np.array(balance_sheet_data["Total ShareHolders Funds"], dtype="f")
    return_on_equity = (net_profit / total_equity) * 100
    years = income_statement_data["YEARS"][::-1]
    return_on_equity = return_on_equity[::-1]
    return_on_equity_graph = plot_graph(years, return_on_equity, "YEARS", "ROE (%)", "line", 12, "#28282B")
    return return_on_equity_graph

# function to plot graph of Debt to Equity (D/E) of a company
def plot_debt_to_equity(balance_sheet_data):
    try:
        total_debt = np.array(balance_sheet_data["Long Term Borrowings"], dtype="f") + \
                        np.array(balance_sheet_data["Short Term Borrowings"], dtype="f")
        total_equity = np.array(balance_sheet_data["Total Shareholders Funds"], dtype="f")
    except Exception as e:
        total_debt = np.array(balance_sheet_data["Borrowings"], dtype="f")
        total_equity = np.array(balance_sheet_data["Total ShareHolders Funds"], dtype="f")
    debt_to_equity = (total_debt / total_equity)
    years = balance_sheet_data["YEARS"][::-1]
    debt_to_equity = debt_to_equity[::-1]
    debt_to_equity_graph = plot_graph(years, debt_to_equity, "YEARS", "Debt-to-Equity", "line", 2)
    return debt_to_equity_graph

if __name__ == "__main__":
    # insert_nifty50_stocklist()
    # print(insert_income_statements_stocks())
    print(insert_balance_sheet_stocks())
