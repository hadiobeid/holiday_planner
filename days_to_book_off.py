import config as cfg
from datetime import date, timedelta

class Days_to_book_off:
    
    def __init__(self, num_of_holidays: int, dates_dict: dict) -> None:
        self.max_working = cfg.MAX_RECOMMENDED_WORKDAYS_BEFORE_HOLIDAY
        self.min_holiday = cfg.RECOMMENDED_MIN_HOLIDAY
        self.num_of_holidays = num_of_holidays
        self.remaining_holidays = num_of_holidays
        self.dates_dict = dates_dict
        self.WEEKEND = cfg.WEEKEND_DAYS
        self.number_of_year_days = len(dates_dict)

    def book_holidays(self):
        self._min_recommended_booker()
        self._weekly_recommendation_booker()
        return self.dates_dict, self.remaining_holidays

    def _check_and_book_a_holiday(self, day_num):
        if 0 == self.dates_dict[day_num][0] and 0 < self.remaining_holidays:
            self.dates_dict[day_num][0] = 1
            self.dates_dict[day_num][2] = 'generated'
            self.remaining_holidays -= 1

    def _left_search(self, current_index: int, holiday_count: int, days_count: int):
        if self.dates_dict[current_index][1] in self.WEEKEND or current_index <= 0:
            return -1, holiday_count, days_count
        return self._left_search(current_index -1, holiday_count + self.dates_dict[current_index][0], days_count + 1)

    def _right_search(self, current_index: int, holiday_count: int, days_count: int):
        if self.dates_dict[current_index][1] in self.WEEKEND or current_index >= self.number_of_year_days:
            return 1, holiday_count, days_count
        return self._right_search(current_index + 1, holiday_count + self.dates_dict[current_index][0], days_count + 1)

    def _left_right_search(self, current_index: int):
        _left_starting_index, _left_holiday_count, _left_days_count = self._left_search(current_index -1, 0, 0)
        _right_starting_index, _right_holiday_count, _right_days_count = self._right_search(current_index + 1, 0, 0)
        if _left_days_count < _right_days_count:
            return _left_starting_index, -1 *(_left_days_count + 1) , -1
        elif _right_days_count < _left_days_count:
            return _right_starting_index, _right_days_count + 1, 1
        return _left_starting_index, -1 * (_left_days_count + 1), -1


    def _min_recommended_booker(self):
        working_days_counter = 0
        for i in range(1, len(self.dates_dict) -1):
            if 0 == self.remaining_holidays:
                break
            j_isholiday = self.dates_dict[i - 1][0]
            i_isholiday = self.dates_dict[i][0]
            k_isholiday = self.dates_dict[i + 1][0]
            if 1 == j_isholiday and 1 == k_isholiday:
                working_days_counter = 0
                if 0 == i_isholiday:
                    self._check_and_book_a_holiday(i)
                continue
            if working_days_counter == self.max_working:
                for n in range(-1, 2):
                    self._check_and_book_a_holiday(i + n)
                working_days_counter = 0
                continue
            working_days_counter += 1


    def _weekly_recommendation_booker(self):
        for i in range(0, len(self.dates_dict) -1):
            if 0 >= self.remaining_holidays:
                break
            if self.dates_dict[i][1] not in self.WEEKEND and 1 == self.dates_dict[i][0]:
                start_index, number_of_days, _step = self._left_right_search(i)
                for j in range(start_index, number_of_days, _step):
                    self._check_and_book_a_holiday(i + j)
