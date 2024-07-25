from flask import Flask, render_template, request, redirect, url_for
from holiday_planner import HolidayPlanner
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
        return redirect(url_for('calendar_view',holidays_number= holidays_number,year= year, country=country))
    else:
        return render_template('index.html')

@app.route('/CalendarView/<holidays_number>/<year>/<country>')
def calendar_view(holidays_number, year, country):
    print(type(holidays_number))
    _year= int(year)
    holiday_planner = HolidayPlanner(int(holidays_number),country ,int(_year))
    holidays, holiday_types, remaining_days = holiday_planner.get_holiday_plan()
    return render_template('calendar_view.html', 
                           holidays = holidays, remaining_days = remaining_days,
                           holiday_types = holiday_types, zip = zip,
                           year=year)
if __name__ == '__main__':
    app.run(debug=True)