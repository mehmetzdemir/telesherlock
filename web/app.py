"""
Flask Web
"""
from flask import Flask, render_template
from flask_gravatar import Gravatar
from webtools import Settings, get_activities, get_users


settings = Settings()
app = Flask(__name__)

gravatar = Gravatar(app, size=128, rating='g', default='retro')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/charts/")
def charts_view():
    activities = get_activities(settings)
    date_range = []  # list of dates for x axis
    chart_series = {}  # list of users with duration for y axis
    for date in activities:
        date_range.append(date)
        for point in activities[date]:
            if point['user'] not in chart_series:
                chart_series[point['user']] = []
            chart_series[point['user']].append(point['duration'])
    return render_template("chart.html", date_range=date_range, chart_series=chart_series)


@app.route("/users/")
def users_view():
    users = get_users(settings)
    return render_template("users.html", users=users)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
