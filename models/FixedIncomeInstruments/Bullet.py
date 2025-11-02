import pandas as pd
from dateutil.relativedelta import relativedelta
from models.FixedIncomeInstruments.Bond import Bond
from utils.utils import newton_raphson_disc

class Bullet(Bond):
    def __init__(self, principal, maturity_date, issue_date, interest_rate, annual_compound=1):
        super().__init__(principal, maturity_date, issue_date, interest_rate)
        self.annual_compound = annual_compound
    
    def rate(self):
        return self.interest_rate / self.annual_compound
    
    
    def total_periods(self):
        return len(self.payment_schedule())
    
    def cashflows(self, start_date):
        cf_df = pd.DataFrame([], columns=["Tau", "Date", "Payment"]) 

        payment_schedule = self.payment_schedule()

        st = self.issue_date if not start_date else start_date
        end = self.maturity_date

        prev_p_date = None
        period = 1
        coupon_value = self.coupon_value()
        for next_p_date in payment_schedule:
            if prev_p_date is None:
                accrued_days = self.acc_interest_convention.diff_days(st, next_p_date) / self.acc_interest_convention.coupon_period(self.annual_compound)
                cf_df.loc[len(cf_df)] = [period, next_p_date, coupon_value / accrued_days]
            else:
                cf_df.loc[len(cf_df)] = [period, next_p_date, coupon_value]
            
            prev_p_date = next_p_date
            period += 1

        cf_df.loc[cf_df.index[-1], "Payment"] += self.maturity_value()
        return cf_df

    def discounted_cashflows(self, start_date=None):
        cf_df = self.cashflows(start_date=start_date)

        cf_df['Discount Factor'] = cf_df["Tau"].apply(self.discount_factor)
        cf_df['Present Value'] = cf_df["Payment"] / cf_df['Discount Factor']
        cf_df.attrs["price"] = cf_df["Present Value"].sum()
        return cf_df
    
    
    def future_value(self, start_date=None):
        cf_df = self.cashflows(start_date=start_date)

        return cf_df["Payment"].sum()

    def coupon_value(self):
        return self.maturity_value() * self.rate()

    def price(self, valuation_date=None):
        df = self.discounted_cashflows(start_date=valuation_date)
        return df["Present Value"].sum()
    
    def payment_schedule(self):
        months = 12 / self.annual_compound

        schedule = []
        current_date = self.maturity_date
        
        while current_date > self.issue_date:
            schedule.append(current_date)
            current_date -= relativedelta(months=months)

        schedule = sorted(schedule) 
        return schedule
    
    def _discount_factor_yearly(self, t):
            return pow(1 + self.interest_rate, t)
    
    def yield_to_maturity(self, price_obs= None, valuation_date=None):
        if not price_obs:
            price_obs = self.price()
        
        if not valuation_date:
            valuation_date = self.issue_date
        cf_df = self.cashflows(start_date=valuation_date)
        cf_df = cf_df[cf_df['Date'] > valuation_date].reset_index(drop=True)
        cf_df['Tau'] = (cf_df.index + 1) / self.annual_compound
        ytm = newton_raphson_disc(price_obs, cf_df[['Tau','Payment']])
        return ytm        


    def current_yield(self):
        return super().current_yield()



            





