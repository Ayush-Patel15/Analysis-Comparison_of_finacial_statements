## IMPORTS
from flask import Flask, render_template, request, redirect, url_for
from db_connect import connect_to_the_database
from main import plot_working_capital, plot_current_ratio, plot_return_on_assets, plot_return_on_equity, plot_debt_to_equity
from main import overall_analysis_nifty

## APP INITIALISATION
app = Flask(__name__)

############ ROUTES ############
# Base path to check the connection
@app.route("/")
def base_function():
    print("Web page is working fine..!")
    return redirect("/home")

# Home page path, or the landing page
@app.route("/home")
def home_page_function():
    db = connect_to_the_database(database="Fundamentals")
    stocks_list = list(db["nifty_list"].find({}))
    if request.args:
        code = request.args.get("code")
    else:
        code = "AE13"
    income_statement = db["income_statements"].find_one({"code": code})
    balance_sheet = db["balance_sheets"].find_one({"code": code})
    stock_name = income_statement["full_name"]
    income_statement_data = income_statement["data"]
    balance_sheet_data = balance_sheet["data"]
    wc_graph = plot_working_capital(balance_sheet_data)
    cr_graph = plot_current_ratio(balance_sheet_data)
    roa_graph = plot_return_on_assets(income_statement_data, balance_sheet_data)
    roe_graph = plot_return_on_equity(income_statement_data, balance_sheet_data)
    de_graph = plot_debt_to_equity(balance_sheet_data)
    return render_template("home.html", stocks_list=stocks_list, income_statement_data=income_statement_data,
                            stock_name=stock_name, balance_sheet_data=balance_sheet_data, de_graph=de_graph,
                            wc_graph=wc_graph, cr_graph=cr_graph, roa_graph=roa_graph, roe_graph=roe_graph)

# Path for overall analysis, and comparison in between the stocks
@app.route("/analysis-and-comparison")
def analysis_and_comparison_function():
    analysis_table = {}
    count_working_capital, count_current_ratio, count_roe, count_de = (0,0,0,0)
    sum_roa, sum_roe = (0,0)
    max_roe = 0
    max_roe_stock = None
    db = connect_to_the_database(database="Fundamentals")
    stocks_list = list(db["nifty_list"].find({}))
    for stock in stocks_list:
        income_statement = db["income_statements"].find_one({"code": stock["code"]})
        balance_sheet = db["balance_sheets"].find_one({"code": stock["code"]})
        mean_lst = overall_analysis_nifty(income_statement["data"], balance_sheet["data"])
        analysis_table[stock["full_name"]] = [round(float(ele), 2) for ele in mean_lst]
    for key in analysis_table:
        if analysis_table[key][0] >= 0:
            count_working_capital += 1
        if analysis_table[key][1] >= 1:
            count_current_ratio += 1
        if analysis_table[key][2]:
            sum_roa += analysis_table[key][2]
        if analysis_table[key][3]:
            sum_roe += analysis_table[key][3]
            if analysis_table[key][3] >= 12:
                count_roe += 1
            if analysis_table[key][3] > max_roe:
                max_roe = analysis_table[key][3]
                max_roe_stock = key
        if analysis_table[key][4] < 2:
            count_de += 1
    average_roa = round(sum_roa/50, 2)
    average_roe = round(sum_roe/50, 2)
    return render_template("analysis_report.html", analysis_table=analysis_table, count_working_capital=count_working_capital,
            count_cuurent_ratio=count_current_ratio, average_roa=average_roa, average_roe=average_roe, count_de=count_de,
            max_roe=max_roe, max_roe_stock=max_roe_stock)

### App run
if __name__ == "__main__":
    app.run()
