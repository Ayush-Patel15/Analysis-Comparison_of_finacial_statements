from bs4 import BeautifulSoup
import requests

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

## function to get rows & heading rows from the main page url
def get_rows_and_heading_rows(page_url):
    response = get_soup(URL=page_url)
    table_section = response.select(".financial-table")[0]
    rows = table_section.select("table tr")
    heading_rows = table_section.select("tr.darkbg")
    return rows, heading_rows

## function to scrape the details of income statement of a stock
def scrape_income_statement_stock(income_statement_url_1, income_statement_url_2):
    result = {}
    rows, heading_rows = get_rows_and_heading_rows(income_statement_url_1)
    result["YEARS"] = [td.text for td in rows[0].select("td")[1:-1]]
    for row in rows[2:]:
        if row not in heading_rows:
            result[row.select("td")[0].text] = [td.text for td in row.select("td")[1:-1]]
    ####### scraping for page 2 ########
    rows, heading_rows = get_rows_and_heading_rows(income_statement_url_2)
    result["YEARS"].extend([td.text for td in rows[0].select("td")[1:-1]])
    for row in rows[2:]:
        if row not in heading_rows:
            try:
                result[row.select("td")[0].text].extend([td.text for td in row.select("td")[1:-1]])
            except Exception as e:
                pass
    return result

## function to scrape the details of balance sheet of a stock
def scrape_balance_sheet_stock(balance_sheet_url_1, balance_sheet_url_2):
    result = {}
    rows, heading_rows = get_rows_and_heading_rows(balance_sheet_url_1)
    result["YEARS"] = [td.text for td in rows[0].select("td")[1:-1]]
    for row in rows[2:]:
        if row not in heading_rows:
            result[row.select("td")[0].text] = [td.text for td in row.select("td")[1:-1]]
    #### scraping for page 2 ####
    rows, heading_rows = get_rows_and_heading_rows(balance_sheet_url_2)
    result["YEARS"].extend([td.text for td in rows[0].select("td")[1:-1]])
    for row in rows[2:]:
        if row not in heading_rows:
            try:
                result[row.select("td")[0].text].extend([td.text for td in row.select("td")[1:-1]])
            except Exception as e:
                pass
    return result

if __name__ == "__main__":
    # print(get_soup(URL="https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"))
    # print(scrape_stocklist_from_indices(indices_url="https://www.moneycontrol.com/markets/indian-indices/changeTableData?exName=N&indicesID=9&selPage=marketTerminal"))
    # print(scrape_income_statement_stock("https://www.moneycontrol.com/financials/adanienterprises/consolidated-profit-lossVI/AE13/1", 
    #         "https://www.moneycontrol.com/financials/adanienterprises/consolidated-profit-lossVI/AE13/2"))
    # print(scrape_income_statement_stock("https://www.moneycontrol.com/financials/statebankindia/consolidated-profit-lossVI/SBI/1", 
    #         "https://www.moneycontrol.com/financials/statebankindia/consolidated-profit-lossVI/SBI/2"))
    # print(scrape_balance_sheet_stock("https://www.moneycontrol.com/financials/adanienterprises/consolidated-balance-sheetVI/AE13/1", 
    #         "https://www.moneycontrol.com/financials/adanienterprises/consolidated-balance-sheetVI/AE13/2"))
    print(scrape_balance_sheet_stock("https://www.moneycontrol.com/financials/statebankindia/consolidated-balance-sheetVI/SBI/1", 
        "https://www.moneycontrol.com/financials/statebankindia/consolidated-balance-sheetVI/SBI/2"))
