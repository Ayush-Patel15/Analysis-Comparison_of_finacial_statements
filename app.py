from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def base_function():
    return "<h2>Web page is working fine..!</h2>"

if __name__ == "__main__":
    app.run(debug=True, port=7070)
