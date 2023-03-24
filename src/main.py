## IMPORTS
from db_connect import connect_to_the_database, insert_and_update_collection
from scraper import scrape_stocklist_from_indices, scrape_income_statement_stock, scrape_balance_sheet_stock
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


if __name__ == "__main__":
    # insert_nifty50_stocklist()
    # print(insert_income_statements_stocks())
    print(insert_balance_sheet_stocks())
