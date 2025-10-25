import pandas as pd
from dateutil.relativedelta import relativedelta
from models.FixedIncomeInstruments.Bond import Bond

class Bullet(Bond):
    def __init__(self, principal, maturity_date, issue_date, interest_rate, annual_compound=1):
        super().__init__(principal, maturity_date, issue_date, interest_rate)
        self.annual_compound = annual_compound
    
    def rate(self):
        return self.interest_rate / self.annual_compound
     
    def future_value(self, periods):
        return self.principal * pow(1 + self.rate(), periods * self.annual_compound)
    
    def total_periods(self):
        return super().total_periods() * self.annual_compound
    
    def cashflows(self):
        cashflows = []
        coupon = self.maturity_value() * self.rate()

        for t in range(1, self.total_periods()):
            value = coupon / self.discount_factor(t)
            cashflows.append((t, value))

        cashflows.append((self.total_periods(), self.maturity_value() / self.discount_factor(self.total_periods())))
        return cashflows
    
    def present_value_of_coupon_annuity(self):
        coupon = self.maturity_value() * self.rate()
        return coupon * self.pvifa(self.total_periods())

    def present_value_of_par(self):
        return self.principal / self.discount_factor(self.total_periods())
    
    def coupon_value(self):
        return self.maturity_value() * self.rate()

    def price(self):
        return self.present_value_of_coupon_annuity() + self.present_value_of_par()
    
    def payment_schedule(self):
        months = 12 / self.annual_compound

        schedule = []
        current_date = self.maturity_date

        
        while current_date > self.issue_date:
            schedule.append(current_date)
            current_date -= relativedelta(months=months)

        schedule = sorted(schedule) 
        return schedule
    
    def cashflow_to_maturity(self, start_date=None):
        """
            Returns a table of future cashflows to maturity
        """
        cf_df = pd.DataFrame([], columns=["Date", "Payment"]) 

        payment_schedule = self.payment_schedule()

        st = self.issue_date if not start_date else start_date
        end = self.maturity_date

        prev_p_date = None
        for next_p_date in payment_schedule:
            if prev_p_date is None:
                accrued_days = self.acc_interest_convention.diff_days(st, next_p_date) / self.acc_interest_convention.coupon_period(self.annual_compound)
                cf_df.loc[len(cf_df)] = [next_p_date, self.coupon_value() / accrued_days]
            else:
                cf_df.loc[len(cf_df)] = [next_p_date, self.coupon_value()]
            
            prev_p_date = next_p_date

        cf_df.loc[cf_df.index[-1], "Payment"] += self.maturity_value()
        return cf_df




            





