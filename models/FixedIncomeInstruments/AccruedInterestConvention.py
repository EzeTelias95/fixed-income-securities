from datetime import date

class AccruedInterestConvention(object):
    def __init__(self):
        pass
    
    def diff_days(self, start_date: date, end_date: date) -> float:
        raise NotImplementedError()

class GovStandard(AccruedInterestConvention):
    def __init__(self):
        super().__init__()

    def diff_days(self, start_date: date, end_date: date) -> float:
        days = (end_date - start_date).days
        year_days = 366 if (start_date.year % 4 == 0 and 
                            (start_date.year % 100 != 0 or start_date.year % 400 == 0)) else 365
        return days / year_days


class MarketStandard(AccruedInterestConvention):
    def __init__(self):
        super().__init__()

    def diff_days(self, start_date: date, end_date: date) -> float:
        y1, m1, d1 = start_date.year, start_date.month, start_date.day
        y2, m2, d2 = end_date.year, end_date.month, end_date.day

        if d1 == 31:
            d1 = 30

        if d2 == 31 and d1 == 30:
            d2 = 30

        days360 = (
            360 * (y2 - y1)
            + 30 * (m2 - m1)
            + (d2 - d1)
        )

        return days360
    
    def coupon_period(self, annual_compound):
        year_days = 360
        days = year_days / annual_compound
        return days
