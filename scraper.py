from bs4 import BeautifulSoup
import requests

NIFTY50_URL = "https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"
SENSEX30_URL = "https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=B&indicesID=4&selPage=marketTerminal"

####### HELPER / GLOBAL FUNCTIONS #######

## function to get the soup of a webpage
def get_soup(URL):
    response = BeautifulSoup(
        requests.get(URL).text,
        "lxml"
    )
    return response

## function to scrape the list of stocks from any of the indices.
def scrape_stocklist_from_indices(indices_url):
    result = []
    response = get_soup(URL=indices_url)
    table = response.select("#indicesTable")[0]
    rows = table.select("tbody tr")
    for row in rows:
        href = row.select("td")[0].select("a")[0]["href"].split("/")
        result.append({
            "full_name": row.select("td")[0].select("a")[0].text,
            "code": href[-1],
            "url_name": href[-2]
        })
    return result

####### HELPER FUNCTIONS #######

# function to scrape the list of nifty 50 stocks
def scrape_nifty50_stocks():
    nifty_stocks = scrape_stocklist_from_indices(indices_url=NIFTY50_URL)
    return nifty_stocks

# function to scrape the list of sensex 30 stocks
def scrape_sensex30_stocks():
    sensex_stocks = scrape_stocklist_from_indices(indices_url=SENSEX30_URL)
    return sensex_stocks

if __name__ == "__main__":
    # get_soup(URL=SENSEX30_URL)
    # scrape_stocklist_from_indices()
    print(scrape_nifty50_stocks())
    print(scrape_sensex30_stocks())