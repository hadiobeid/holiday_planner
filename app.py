from flask import Flask, render_template

app = Flask('Holiday Planner')


@app.route('/')
def calendar_view():
    return render_template('index.html')
