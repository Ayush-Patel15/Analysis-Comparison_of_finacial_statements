## IMPORTS
from flask import Flask, render_template, request, redirect, url_for
from db_connect import connect_to_the_database

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
    income_statement_data = income_statement["data"]
    stock_name = income_statement["full_name"]
    return render_template("home.html", stocks_list=stocks_list, income_statement_data=income_statement_data, 
                            stock_name=stock_name)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
