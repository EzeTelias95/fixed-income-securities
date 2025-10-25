from datetime import datetime as dt
from models.FixedIncomeInstruments.AccruedInterestConvention import MarketStandard

class Bond(object):
    def __init__(self, principal, maturity_date, issue_date, interest_rate):
        self.principal = principal
        self.maturity_date = dt.strptime(maturity_date, "%Y-%m-%d")      
        self.issue_date = dt.strptime(issue_date, "%Y-%m-%d")    
        self.interest_rate = interest_rate
        self.acc_interest_convention = MarketStandard()
    
    def rate(self):
        raise NotImplemented
    
    def future_value(self, periods):
        raise NotImplemented
    
    def present_value(self, future_value_expected, periods):
        return future_value_expected * (1 / pow(1 + self.rate(), periods))
    
    def maturity_value(self):
        return self.principal
    
    def total_periods(self):
        return self.maturity_date.year - self.issue_date.year
    
    def discount_factor(self, t):
        return pow(1 + self.rate(), t)

    def pvifa(self, n):
        """Present Value Interest Factor of Annuity """
        return (1 - (1 / self.discount_factor(n))) / self.rate()
    
    def price(self):
        raise NotImplemented
    
    def payment_schedule(self):
        return [self.maturity_date] 
    
















    
    # def PresentValueOfFutureValueSeries(self, future_value_expected, coupon, periods):
    #     series = []
    #     for t in range(1, periods):
    #         value = coupon / pow( 1 + self.Rate(), t)
    #         series.append((t,value))
        

    #     series.append((periods, (coupon + future_value_expected) / pow( 1 + self.Rate(), periods) ))
    #     return series
    
    # def PresentValueOfFutureValues(self, future_value_expected, coupon, periods):
    #     series = self.PresentValueOfFutureValueSeries(future_value_expected, coupon, periods)

    #     return sum(v for _, v in series)
    
    # def PresentValueOfAnnuity(self, annuity, periods):
    #     return annuity * ( (1 - 1/ pow(1 + self.Rate(), periods)) / self.Rate() )
