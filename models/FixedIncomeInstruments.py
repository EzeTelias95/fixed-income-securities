from datetime import datetime

class VanillaBond(object):
    def __init__(self, principal, maturity_date, issue_date, interest_rate):
        self.principal = principal
        self.maturity_date = datetime.strptime(maturity_date, "%Y-%m-%d")      
        self.issue_date = datetime.strptime(issue_date, "%Y-%m-%d")    
        self.interest_rate = interest_rate
    
    def Rate(self):
        raise NotImplemented
    
    def FutureValue(self, periods):
        raise NotImplemented
    
    def PresentValue(self, future_value_expected, periods):
        return future_value_expected * ( 1 / pow( 1 + self.Rate(), periods))
    
    def MaturityValue(self):
        return self.principal
    
    def TotalPeriods(self):
        return self.maturity_date.year - self.issue_date.year
    
    def DiscountFactor(self, t):
        return pow( 1 + self.Rate(), t)

    def PVIFA(self, n):
        """Present Value Interest Factor of Annuity """
        return ( (1 - ( 1 / self.DiscountFactor(n))) / self.Rate())
    
    def Price(self):
        raise NotImplemented
    
class ZeroCoupon(VanillaBond):
    def __init__(self, principal, maturity_date, issue_date, interest_rate):
        super().__init__(principal, maturity_date, issue_date, interest_rate)
    
    def Rate(self):
        return self.interest_rate

    def FutureValue(self, periods):
        return self.principal * pow( 1 + self.Rate(), periods)

    def TotalPeriodsToDiscount(self):
        return self.TotalPeriods() * 2
    
    def DiscountRate(self):
        return self.Rate() / 2
    
    def DiscountFactor(self, t):
        return pow( 1 + self.DiscountRate(), t)
    
    def Price(self):
        return self.MaturityValue() / self.DiscountFactor(self.TotalPeriodsToDiscount())
    
class Bullet(VanillaBond):
    def __init__(self, principal, maturity_date, issue_date, interest_rate, annual_compound=1):
        super().__init__(principal, maturity_date, issue_date, interest_rate)
        self.annual_compound = annual_compound
    
    def Rate(self):
        return self.interest_rate / self.annual_compound
     
    def FutureValue(self, periods):
        return self.principal * pow( 1 + self.Rate(), periods * self.annual_compound)
    
    def TotalPeriods(self):
        return super().TotalPeriods() * self.annual_compound
    
    def Cashflows(self):
        cashflows = []
        coupon = self.MaturityValue() * self.Rate()

        for t in range(1, self.TotalPeriods()):
            value = coupon / self.DiscountFactor(t)
            cashflows.append((t, value))

        cashflows.append((self.TotalPeriods(), self.MaturityValue() / self.DiscountFactor(self.TotalPeriods()) ))
        return cashflows
    
    def PresentValueOfCoupon_Annuity(self):
        coupon = self.MaturityValue() * self.Rate()
        return coupon * self.PVIFA(self.TotalPeriods())

    def PresentValueOfPar(self):
        return self.principal / self.DiscountFactor(self.TotalPeriods())

    def Price(self):
        return self.PresentValueOfCoupon_Annuity() + self.PresentValueOfPar()


















    
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
