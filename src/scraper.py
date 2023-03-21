from bs4 import BeautifulSoup
import requests

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

def scrape_balance_sheet_stock(balance_sheet_url_1, balance_sheet_url_2):
    result = {
        "YEARS": [],
        "SHAREHOLDERS FUND": {},
        "NON-CURRENT LIABILITIES": {},
        "CURRENT LIABILITIES": {},
        "NON-CURRENT ASSETS": {},
        "CURRENT ASSETS": {},
        "CONTINGENT LIABILITIES": {},
        "BONUS DETAILS": {},
        "NON-CURRENT INVESTMENTS": {},
        "CURRENT INVESTMENTS": {}
    }
    response_1 = get_soup(balance_sheet_url_1)
    balance_section_1 = response_1.select(".financial-table")[0]
    rows = balance_section_1.select("table tr")
    result["YEARS"] = [td.text for td in rows[0].select("td")[1:-1]]
    result["SHAREHOLDERS FUND"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[4:10]}
    result["NON-CURRENT LIABILITIES"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[11:16]}
    result["CURRENT LIABILITIES"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[17:23]}
    result["NON-CURRENT ASSETS"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[25:34]}
    result["CURRENT ASSETS"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[35:43]}
    result["CONTINGENT LIABILITIES"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[45:46]}
    result["BONUS DETAILS"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[47:48]}
    result["NON-CURRENT INVESTMENTS"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[49:51]}
    result["CURRENT INVESTMENTS"] = {tr.select("td")[0].text: [td.text for td in tr.select("td")[1:-1]] for tr in rows[52:]}
    #### scraping for page 2 ####
    response_2 = get_soup(balance_sheet_url_2)
    balance_section_2 = response_2.select(".financial-table")[0]
    rows = balance_section_2.select("table tr")
    result["YEARS"].extend([td.text for td in rows[0].select("td")[1:-1]])
    for tr in rows[4:10]:
        result["SHAREHOLDERS FUND"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[11:16]:
        result["NON-CURRENT LIABILITIES"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[17:23]:
        result["CURRENT LIABILITIES"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[25:34]:
        result["NON-CURRENT ASSETS"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[35:43]:
        result["CURRENT ASSETS"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[45:46]:
        result["CONTINGENT LIABILITIES"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[47:48]:
        result["BONUS DETAILS"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[49:51]:
        result["NON-CURRENT INVESTMENTS"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    for tr in rows[52:]:
        result["CURRENT INVESTMENTS"][tr.select("td")[0].text].extend([td.text for td in tr.select("td")[1:-1]])
    return result

if __name__ == "__main__":
    # print(get_soup(URL="https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"))
    # print(scrape_stocklist_from_indices(indices_url="https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"))
    # print(scrape_income_statement_stock("https://www.moneycontrol.com/financials/adanienterprises/consolidated-profit-lossVI/AE13/1", 
    #         "https://www.moneycontrol.com/financials/adanienterprises/consolidated-profit-lossVI/AE13/2"))
    print(scrape_balance_sheet_stock("https://www.moneycontrol.com/financials/adanienterprises/consolidated-balance-sheetVI/AE13/1", 
            "https://www.moneycontrol.com/financials/adanienterprises/consolidated-balance-sheetVI/AE13/2"))
