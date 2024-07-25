import config as cfg
from datetime import date, timedelta

class Days_to_book_off:
    
    def __init__(self, num_of_holidays: int, dates_dict: dict) -> None:
        self.max_working = cfg.MAX_RECOMMENDED_WORKDAYS_BEFORE_HOLIDAY
        self.min_holiday = cfg.RECOMMENDED_MIN_HOLIDAY
        self.num_of_holidays = num_of_holidays
        self.remaining_holidays = num_of_holidays
        self.dates_dict = dates_dict

    def _check_and_book_a_holiday(self, day_num):
        if 0 == self.dates_dict[day_num][0] and 0 < self.remaining_holidays:
            self.dates_dict[day_num][0] = 1
            self.dates_dict[day_num][2] = 'generated'
            self.remaining_holidays -= 1

    def min_recommended_booker(self):
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
        return self.dates_dict, self.remaining_holidays
                
            
            
            