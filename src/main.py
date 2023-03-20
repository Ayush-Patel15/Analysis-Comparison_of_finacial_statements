from db_connect import connect_to_the_database, insert_and_update_collection
from scraper import scrape_stocklist_from_indices

NIFTY50_URL = "https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"

# function to insert the list of nifty 50 stocks
def insert_nifty50_stocklist():
    nifty_stocks = scrape_stocklist_from_indices(indices_url=NIFTY50_URL)
    db = connect_to_the_database(database="Fundamentals")
    for stock in nifty_stocks:
        print(insert_and_update_collection(db, "nifty_list", "code", stock))
    return nifty_stocks

if __name__ == "__main__":
    insert_nifty50_stocklist()