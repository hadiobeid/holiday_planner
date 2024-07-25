from flask import Flask, render_template
from holiday_planner import HolidayPlanner
app = Flask('Holiday Planner')


@app.route('/')
def calendar_view():
    holiday_planner = HolidayPlanner()
    holidays, holiday_types, remaining_days = holiday_planner.get_holiday_plan()
    return render_template('index.html', holidays = holidays, remaining_days = remaining_days, holiday_types = holiday_types, zip = zip)
