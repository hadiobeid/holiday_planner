import config as cfg
import pandas as pd
from datetime import datetime, date, timedelta
from days_to_book_off import Days_to_book_off

class HolidayPlanner:
    def __init__(self, Number_of_holidays, country, state, year, max_workdays, min_holidays, weekend_days: list) -> None:
        # TODO: Remove later this is only test values
        self.year = year
        self.country = country
        self.state = state
        self.Number_of_holidays = Number_of_holidays
        self.max_workdays = max_workdays
        self.min_holidays = min_holidays
        self.weekend_days = weekend_days
        print(self.weekend_days)
        
    def _get_all_dates_between_two_date(self, year: int) -> list:
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
        
        days_range = range(int((end_date - start_date).days) + 1)
        for i in days_range:
            temp_date = start_date + timedelta(days=i)
            all_dates.append(temp_date)
            all_days_names.append(temp_date.strftime("%A"))
            
        return all_dates, all_days_names, days_range

    def _get_date_from_date_string(self, date_str: list, year) -> list:
        dates = []
        for i in date_str:
            splited = str(i).split(' ')
            month_num = cfg.MONTH_AND_NUM[splited[0]]
            day = int(splited[1])
            dates.append(date(year, month_num, day))
        return dates

    def _get_country_holidays(self) -> list:
        url = cfg.BANK_HOLIDAYS_URL + self.country + self.state + '/' + str(self.year)
        _df = pd.read_html(url)[0]
        _df = _df[~_df['Type'].isin(['Not A Public Holiday'])]
        dates_list = _df['Date'].to_list()
        return self._get_date_from_date_string(dates_list, self.year)

    
    def get_holiday_plan(self):
        all_dates, all_date_names, days_range = self._get_all_dates_between_two_date(self.year)
        country_holidays = self._get_country_holidays()
        dates_dict = []
        for i_date, date_name in zip(all_dates, all_date_names):
            isholiday = 1 if i_date in country_holidays or date_name in self.weekend_days else 0
            day_type = 'normal'
            if 1 == isholiday and not date_name in self.weekend_days:
                day_type = 'bank holiday'
            dates_dict.append([isholiday, date_name, day_type])
        _dates_dict, remaining_days = Days_to_book_off(self.Number_of_holidays, dates_dict,
                                                       self.max_workdays, self.min_holidays, self.weekend_days).book_holidays()
        print(remaining_days)

        holidays_dates_list = []
        day_types = []
        i = 0
        for value in _dates_dict:
            if 1 == value[0] and value[1] not in self.weekend_days:
                day_types.append(value[2])
                holidays_dates_list.append(str(all_dates[i]))
            i += 1
        # TODO: Remove later this is only for testing
        return holidays_dates_list, day_types, remaining_days
        
    
