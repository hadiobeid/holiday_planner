from flask import Flask, render_template, request, redirect, url_for
from holiday_planner import HolidayPlanner
import json
import countries_states as cs
app = Flask('Holiday Planner')

global_holidays_number = 0
global_year = 2024
global_country = ''

@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        holidays_number = request.form.get("available_holidays")
        year = int(request.form.get("selected_year"))
        print(type(year))
        country = request.form.get("selected_country")
        state = request.form.get("states_select") if request.form.get("states_select") else ''
        return redirect(url_for('calendar_view',holidays_number= holidays_number,year= year, country=country, state=state))
    else:
        return render_template('index.html', country_states = cs.countries_state_dict)

@app.route('/CalendarView/<holidays_number>/<year>/<country>/<state>')
def calendar_view(holidays_number, year, country, state):
    print(type(holidays_number))
    _year= int(year)
    holiday_planner = HolidayPlanner(int(holidays_number),country, state, int(_year))
    holidays, holiday_types, remaining_days = holiday_planner.get_holiday_plan()
    return render_template('calendar_view.html', 
                           holidays = holidays, remaining_days = remaining_days,
                           holiday_types = holiday_types, zip = zip,
                           year=year)

if __name__ == '__main__':
    app.run(debug=True)