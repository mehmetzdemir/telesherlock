"""
Flask Web
"""
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/charts")
def charts():
    data = {
        'aybuke_online': [7.0, 6.9, 9.1, 14.5, 18.4, 21.5, 25.2],
        'halil_online': [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0]
    }
    return render_template("chart.html", **data)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
