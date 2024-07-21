import config as cfg
import requests as r
import pandas as pd
from datetime import datetime, date, timedelta

def _get_all_dates_between_two_date(year: int) -> list:
    """Get all Dates in a year, and names of those dates

    Args:
        year (int): the year to get all the dates for

    Returns:
        list: all the dates in that year
        list: names of all dates in order
    """
    start_date = date(year, 1,1)
    end_date = date(year, 12,31)
    all_dates = []
    all_days_names = []
    for i in range(int((end_date - start_date).days) + 1):
        temp_date = start_date + timedelta(days=i)
        all_dates.append(temp_date)
        all_days_names.append(temp_date.strftime("%A"))
    return all_dates, all_days_names

def _get_date_from_date_string(date_str: list, year) -> list:
    dates = []
    for i in date_str:
        splited = str(i).split(' ')
        month_num = cfg.MONTH_AND_NUM[splited[0]]
        day = int(splited[1])
        dates.append(date(year, month_num, day))
    return dates

def _get_country_holidays(country: str, year: int) -> list:
    url = cfg.BANK_HOLIDAYS_URL + country + '/' + str(year)
    dates_list = pd.read_html(url)[0]['Date'].to_list()
    return _get_date_from_date_string(dates_list, year)

# TODO: Remove later this is only test values
year = datetime.now().year
country = 'united-kingdom'
Number_of_holidays = 22

all_dates, all_date_names = _get_all_dates_between_two_date(year)
country_holidays = _get_country_holidays(country, year)
dates_dict = {}
for i_date, date_name in zip(all_dates, all_date_names):
    isholiday = 1 if i_date in country_holidays or date_name in cfg.WEEKEND_DAYS else 0
    dates_dict[str(i_date)] = [isholiday, date_name]

# TODO: Remove later this is only for testing
df = pd.DataFrame(dates_dict)
df.to_csv('./test.csv', index=False)
