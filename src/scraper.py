from db_connect import connect_to_the_database, insert_and_update_collection
from bs4 import BeautifulSoup
from datetime import datetime
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

def scrape_income_statement_stock(income_statement_url_1, income_statement_url_2):
    result = {
        "YEARS": [],
        "INCOME": {},
        "EXPENSES": {},
        "TAX EXPENSES-CONTINUED OPERATIONS": {},
        "EARNINGS PER SHARE": {},
        "DIVIDEND": {}
    }
    response_1 = get_soup(URL=income_statement_url_1)
    income_section_1 = response_1.select(".financial-table")[0]
    rows = income_section_1.select("table tr")
    rows.pop(33)    # Popping the not required row from rows list
    result["YEARS"] = [td.text for td in rows[0].select("td")[1:-1]]
    result["INCOME"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[3:9]}
    result["EXPENSES"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[10:22]}
    result["TAX EXPENSES-CONTINUED OPERATIONS"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[23:33]}
    result["EARNINGS PER SHARE"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[34:36]}
    result["DIVIDEND"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[37:]}
    #### scraping for page 2 ####
    response_2 = get_soup(URL=income_statement_url_2)
    income_section_2 = response_2.select(".financial-table")[0]
    rows = income_section_2.select("table tr")
    rows.pop(33)    # Popping the not required row from rows list
    result["YEARS"].extend([td.text for td in rows[0].select("td")[1:-1]])
    for tr in rows[3:9]:
        result["INCOME"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[10:22]:
        result["EXPENSES"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[23:33]:
        result["TAX EXPENSES-CONTINUED OPERATIONS"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[34:36]:
        result["EARNINGS PER SHARE"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[37:]:
        result["DIVIDEND"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    return result

####### MAIN SECTION #######

# function to scrape the list of nifty 50 stocks
def scrape_and_insert_nifty50_stocklist():
    nifty_stocks = scrape_stocklist_from_indices(indices_url=NIFTY50_URL)
    db = connect_to_the_database(database="Fundamentals")
    for stock in nifty_stocks:
        stock["created_at"] = datetime.now()
        print(insert_and_update_collection(db, "nifty_list", "code", stock))
    return nifty_stocks

if __name__ == "__main__":
    # get_soup(URL=SENSEX30_URL)
    # scrape_stocklist_from_indices()
    # scrape_and_insert_nifty50_stocklist()
    print(scrape_income_statement_stock("https://www.moneycontrol.com/financials/adanienterprises/consolidated-profit-lossVI/AE13/1", 
            "https://www.moneycontrol.com/financials/adanienterprises/consolidated-profit-lossVI/AE13/2"))
    