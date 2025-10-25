from models.FixedIncomeInstruments.Bond import Bond

class ZeroCoupon(Bond):
    def __init__(self, principal, maturity_date, issue_date, interest_rate):
        super().__init__(principal, maturity_date, issue_date, interest_rate)
    
    def rate(self):
        return self.interest_rate

    def future_value(self, periods):
        return self.principal * pow(1 + self.rate(), periods)

    def total_periods_to_discount(self):
        """ Semi annual"""
        return self.total_periods() * 2
    
    def discount_rate(self):
        return self.rate() / 2
    
    def discount_factor(self, t):
        return pow(1 + self.discount_rate(), t)
    
    def price(self):
        return self.maturity_value() / self.discount_factor(self.total_periods_to_discount())
    
