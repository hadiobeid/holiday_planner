import config as cfg
import pandas as pd
from datetime import datetime, date, timedelta
from days_to_book_off import Days_to_book_off

class HolidayPlanner:
    def __init__(self, Number_of_holidays, country, state, year, max_workdays, min_holidays, weekend_days: list, selected_days_off: list) -> None:
        # Year to book holidays in
        self.year = year
        # country to get public holidays for
        self.country = country
        # state of that country if applicable
        self.state = state
        # Number of available holiday to book off
        self.Number_of_holidays = Number_of_holidays
        # the Max number of days before requiring to book at least the min holiday
        self.max_workdays = max_workdays
        # Min number of holiday to re-energies
        self.min_holidays = min_holidays
        # List of weekend days
        self.weekend_days = weekend_days
        # List of dates the user wants to book of
        self.selected_days_off = []
        # fill the self.selected_days_off with the dates the user selected
        # if applicable
        if len(selected_days_off)> 0:
            for selected in selected_days_off:
                # change the string to date
                self.selected_days_off.append(datetime.strptime(selected, '%Y-%m-%d').date())
        
    def _get_all_dates_between_two_date(self) -> list:
        """Get all Dates in a year, and names of those dates

        Returns:
            list: all the dates in that year
            list: names of all dates in order
        """
        # start date of the year
        start_date = date(self.year, 1,1)
        # last date in a the year
        end_date = date(self.year, 12,31)
        all_dates = []
        all_days_names = []
        # list of all days 0 to 364 (365 days) or 365 (366 days)
        days_range = range(int((end_date - start_date).days) + 1)
        for i in days_range:
            # date added
            temp_date = start_date + timedelta(days=i)
            all_dates.append(temp_date)
            # day at the date. e.g: Sunday
            all_days_names.append(temp_date.strftime("%A"))
            
        return all_dates, all_days_names, days_range

    def _get_date_from_date_string(self, date_str: list) -> list:
        """The website have the dates as string in a specific format,
           this function change it from string to actual date

        Args:
            date_str (list): list of dates of public holiday each as a string
            year (int): Year

        Returns:
            list: List of public holidays dates
        """
        dates = []
        for i in date_str:
            splited = str(i).split(' ')
            month_num = cfg.MONTH_AND_NUM[splited[0]]
            day = int(splited[1])
            dates.append(date(self.year, month_num, day))
        return dates

    def _get_country_holidays(self) -> list:
        """Get the country public holiday

        Returns:
            list: list of publich holiday dates
        """
        # URL to get the holidays
        url = cfg.BANK_HOLIDAYS_URL + self.country + self.state + '/' + str(self.year)
        # table of holidays
        _df = pd.read_html(url)[0]
        # remove none public holidays from the table
        _df = _df[~_df['Type'].isin(['Not A Public Holiday'])]
        # get the dates as a list
        dates_list = _df['Date'].to_list()
        # change the list of string date to list of dates and return it 
        return self._get_date_from_date_string(dates_list)

    
    def get_holiday_plan(self):
        """Get the plan of those holidays

        Returns:
            holidays_dates_list: list of holidays
            day_types: type of this holiday ['Selected', 'generated', 'bank holiday']
            remaining_days: remaining holidays available for the user
        """
        # get all the dates in a year used because feb might have 29 days
        all_dates, all_date_names, days_range = self._get_all_dates_between_two_date()
        # get the holiday dates of specified country
        country_holidays = self._get_country_holidays()
        dates_dict = []
        for i_date, date_name in zip(all_dates, all_date_names):
            # 0 means it is a working day
            isholiday = 0
            # if the date in holiday list, in weekend days or (is selected by user and they still have days to book of) 
            if (i_date in country_holidays) or (date_name in self.weekend_days) or (i_date in self.selected_days_off and 0 < self.Number_of_holidays):
                isholiday = 1
            # by default set to normal working day
            day_type = 'normal'
            if 1 == isholiday:
                if i_date in self.selected_days_off and 0 < self.Number_of_holidays:
                    # set as selected and reduce the number of holiday they have available to book
                    day_type = 'Selected'
                    self.Number_of_holidays -= 1
                elif not date_name in self.weekend_days:
                    # if it is not in weekend days it has to be public holiday at this point
                    day_type = 'bank holiday' 
            # add it to the list
            dates_dict.append([isholiday, date_name, day_type])
            # run the algorithm to book days off
        _dates_dict, remaining_days = Days_to_book_off(self.Number_of_holidays, dates_dict,
                                                       self.max_workdays, self.min_holidays, self.weekend_days).book_holidays()

        holidays_dates_list = []
        day_types = []
        i = 0
        for value in _dates_dict:
            if 1 == value[0] and value[1] not in self.weekend_days:
                day_types.append(value[2])
                holidays_dates_list.append(str(all_dates[i]))
            i += 1
        return holidays_dates_list, day_types, remaining_days
