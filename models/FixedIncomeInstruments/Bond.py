from datetime import datetime as dt
from models.FixedIncomeInstruments.AccruedInterestConvention import MarketStandard

class Bond(object):
    def __init__(self, principal, maturity_date, issue_date, interest_rate, put_option_date=None, call_option_date=None):
        self.principal = principal
        self.maturity_date = dt.strptime(maturity_date, "%Y-%m-%d")      
        self.issue_date = dt.strptime(issue_date, "%Y-%m-%d")    
        self.interest_rate = interest_rate
        self.acc_interest_convention = MarketStandard()
        self.put_option_date = put_option_date
        self.call_option_date = call_option_date
    
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
    
    def current_yield(self):
        raise NotImplemented
    
    def yield_to_maturity(self):
        raise NotImplemented
    
    def yield_to_call(self):
        if (not self.call_option_date):
            raise Exception("There is no CALL option right set up")
    
    def yield_to_put(self):
        if (not self.put_option_date):
            raise Exception("There is no PUT option right set up")
        
    def TIR(self):
        raise NotImplemented