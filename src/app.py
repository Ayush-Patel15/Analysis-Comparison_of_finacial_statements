## IMPORTS
from flask import Flask, render_template, request, redirect, url_for
from db_connect import connect_to_the_database
from main import plot_working_capital, plot_current_ratio, plot_return_on_assets, plot_return_on_equity

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
    return render_template("home.html", stocks_list=stocks_list, income_statement_data=income_statement_data, 
                            stock_name=stock_name, balance_sheet_data=balance_sheet_data,
                            wc_graph=wc_graph, cr_graph=cr_graph, roa_graph=roa_graph, roe_graph=roe_graph)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
