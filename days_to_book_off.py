import config as cfg
from datetime import date, timedelta

class Days_to_book_off:
    
    def __init__(self, num_of_holidays: int, dates_dict: dict, max_workdays: int, min_holidays: int, weekend_days: list) -> None:
        self.max_working = max_workdays
        self.min_holiday = min_holidays
        self.num_of_holidays = num_of_holidays
        self.remaining_holidays = num_of_holidays
        self.dates_dict = dates_dict
        self.WEEKEND = weekend_days
        self.min_days_off_a_week = len(weekend_days)
        self.number_of_year_days = len(dates_dict) - 1

    def book_holidays(self):
        # runs both algorithms on the dates
        self._min_recommended_booker()
        self._weekly_recommendation_booker()
        return self.dates_dict, self.remaining_holidays

    def _check_and_book_a_holiday(self, day_num):
        # check if the date that to be booked off is not already off 
        # And the user have avaiable day to book off
        if 0 == self.dates_dict[day_num][0] and 0 < self.remaining_holidays:
            self.dates_dict[day_num][0] = 1
            self.dates_dict[day_num][2] = 'generated'
            self.remaining_holidays -= 1

    def _left_search(self, current_index: int, holiday_count: int, days_count: int):
        # search for any day of the week end to the left of the current index
        if self.dates_dict[current_index][1] in self.WEEKEND or current_index <= 0:
            return -1, holiday_count, days_count
        # not found search the left of this index
        return self._left_search(current_index -1, holiday_count + self.dates_dict[current_index][0], days_count + 1)

    def _right_search(self, current_index: int, holiday_count: int, days_count: int):
        # search for any day of the week end to the right of the current index
        if self.dates_dict[current_index][1] in self.WEEKEND or current_index >= self.number_of_year_days:
            return 1, holiday_count, days_count
        # not found search the right of this index
        return self._right_search(current_index + 1, holiday_count + self.dates_dict[current_index][0], days_count + 1)

    def _left_right_search(self, current_index: int):
        # search for the closes weekend day if it is to the left or right
        # search to the left
        _left_starting_index, _left_holiday_count, _left_days_count = self._left_search(current_index -1, 0, 0)
        #search to the right
        _right_starting_index, _right_holiday_count, _right_days_count = self._right_search(current_index + 1, 0, 0)
        if _right_days_count < _left_days_count:
            # if it is closer to the right, return the right output
            return _right_starting_index, _right_days_count + 1, 1
        # return the left output ifn they are equal or left is closer
        return _left_starting_index, -1 * (_left_days_count + 1), -1


    def _min_recommended_booker(self):
        """book the minimum holidays that the user need to re-energies during a year
        """
        working_days_counter = 0
        i = 0
        while i <= self.number_of_year_days:
            if 0 == self.remaining_holidays:
                break
            days = []
            j = 0
            while i +j <= self.number_of_year_days and j < self.min_holiday:
                days.append(self.dates_dict[i + j][0])
                j += 1
            # if the number of days off is higher than weekend days 
            # then there has to be a holiday and it is good to book it off
            # or if the maximum number of days is reached to require
            # re-energising
            if sum(days) > self.min_days_off_a_week or working_days_counter >= self.max_working:
                # set the counter back to 0
                working_days_counter = 0
                # book those dates off
                for n in range(0, j):
                    self._check_and_book_a_holiday(i + n)
                # add the number booked of to i in order to skip them in the next loop
                i += j
                continue
            # no day book off move to the next day and add 1 day to the counter
            i += 1
            working_days_counter += 1

    def _weekly_recommendation_booker(self):
        """check for any day that is a holiday, then check if the weekend day is around it to book any day between them off
        """
        for i in range(0, len(self.dates_dict) -1):
            #check if the user can still book days off
            if 0 >= self.remaining_holidays:
                break
            # if the day is not a weekend and it is a holiday
            if self.dates_dict[i][1] not in self.WEEKEND and 1 == self.dates_dict[i][0]:
                # search for thhe neariest weekend day (left or right of this day)
                start_index, number_of_days, _step = self._left_right_search(i)
                # for to the left/right of this day and book them off
                for j in range(start_index, number_of_days, _step):
                    self._check_and_book_a_holiday(i + j)
