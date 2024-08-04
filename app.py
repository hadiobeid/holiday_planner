from flask import Flask, render_template, request, redirect, url_for
from holiday_planner import HolidayPlanner
import json
import config as cfg
app = Flask('Holiday Planner')

global_holidays_number = 0
global_year = 2024
global_country = ''

def get_weekend_list_days(weekend_str: str):
    """Change string of which day the person has a weekend in to a list
    that string is retrived in the form of a list '[None,None,'on']'
    Args:
        weekend_str (str): string representing which day the person has a weekend in

    Returns:
        list: list of days that are weekend for the user
    """
    weekend_str = weekend_str.replace('[', '')
    weekend_str = weekend_str.replace(']', '')
    weekend_str = weekend_str.replace(' ', '')
    weekend_str = weekend_str.replace("'", '')
    weekend_list = weekend_str.split(',')
    weekend_days = []
    for ischecked, day in zip(weekend_list, cfg.WEEK_DAYS):
        if ischecked == 'on':
            weekend_days.append(day)
    return weekend_days

def get_selected_dates_off(selected_dates_off: str):
    """Change the string of dates the user wants off to list of strings

    Args:
        selected_dates_off (str): string holding all the dates the user wants to book off. those dates are separated by comma

    Returns:
        list: list of dates (str) the user wants off
    """
    if selected_dates_off == 'None':
        return []
    return selected_dates_off.split(',')
    

@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        holidays_number = request.form.get("available_holidays")
        year = int(request.form.get("selected_year"))
        country = request.form.get("selected_country")
        state = request.form.get("states_select") if request.form.get("states_select") else 'All'
        _selected_days_off = request.form.get("selected_off") if request.form.get("selected_off") != '' else 'None'
        _max_workdays = request.form.get("max_days")
        _min_holidays = request.form.get("min_holidays")
        _weekend_days = [request.form.get("Monday"), request.form.get("Tuesday"), request.form.get("Wednesday"),
                         request.form.get("Thursday"), request.form.get("Friday"), request.form.get("Saturday"),
                         request.form.get("Sunday")]
        
        return redirect(url_for('calendar_view',holidays_number= holidays_number,
                                year= year, country=country, state=state,
                                max_workdays=_max_workdays, min_holidays=_min_holidays, weekend_days=_weekend_days, 
                                selected_days_off = _selected_days_off))
    else:
        return render_template('index.html', country_states = cfg.COUNTRIES_STATE_DICT)


@app.route('/CalendarView/<holidays_number>/<year>/<country>/<state>/<max_workdays>/<min_holidays>/<weekend_days>/<selected_days_off>')
def calendar_view(holidays_number, year, country, state, max_workdays, min_holidays, weekend_days, selected_days_off):
    _year= int(year)
    max_workdays = int(max_workdays)
    min_holidays = int(min_holidays)
    state = '/' + state if state != 'All' else ''
    weekend_days = get_weekend_list_days(weekend_days)
    selected_days_off = get_selected_dates_off(selected_days_off)
    holiday_planner = HolidayPlanner(int(holidays_number),country, state, int(_year), max_workdays, min_holidays, weekend_days, selected_days_off)
    holidays, holiday_types, remaining_days = holiday_planner.get_holiday_plan()
    return render_template('calendar_view.html', 
                           holidays = holidays, remaining_days = remaining_days,
                           holiday_types = holiday_types, zip = zip,
                           weekend_days = weekend_days,
                           year=year)

if __name__ == '__main__':
    app.run(debug=True)