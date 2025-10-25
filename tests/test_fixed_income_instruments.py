import math
import pytest

from fixed-income-securities.models.FixedIncomeInstruments import (
    VanillaBond,
    ZeroCoupon,
    Bullet,
)


def test_vanilla_bond_initialization_and_total_periods():
    vb = VanillaBond(1000, "2030-01-01", "2020-01-01", 0.10)
    assert vb.principal == 1000
    assert vb.maturity_date.year == 2030
    assert vb.issue_date.year == 2020
    assert vb.TotalPeriods() == 10


def test_zero_coupon_price_and_rates():
    zc = ZeroCoupon(1000, "2026-01-01", "2024-01-01", 0.06)
    # Semi-annual discounting
    assert math.isclose(zc.DiscountRate(), 0.03)
    assert zc.TotalPeriodsToDiscount() == (zc.TotalPeriods() * 2)
    expected_df = (1 + 0.03) ** (zc.TotalPeriodsToDiscount())
    assert math.isclose(zc.DiscountFactor(zc.TotalPeriodsToDiscount()), expected_df)
    expected_price = 1000 / expected_df
    assert math.isclose(zc.Price(), expected_price)


def test_bullet_bond_basic_cashflows_and_price():
    b = Bullet(1000, "2027-01-01", "2024-01-01", 0.12, annual_compound=2)
    # Rate per period
    assert math.isclose(b.Rate(), 0.06)
    # Total periods should scale with compounding frequency
    assert b.TotalPeriods() == (2027 - 2024) * 2

    # Coupon per period
    coupon = b.MaturityValue() * b.Rate()  # 1000 * 0.06 = 60

    # Cashflows include coupon PVs for periods 1..N-1 and par at N
    cfs = b.Cashflows()
    N = b.TotalPeriods()
    assert len(cfs) == N  # N-1 coupon entries + 1 par entry

    # Validate the last cashflow is par discounted at N
    t_last, pv_last = cfs[-1]
    assert t_last == N
    assert math.isclose(pv_last, b.MaturityValue() / b.DiscountFactor(N))

    # PV of coupon annuity matches method
    pv_coupons = b.PresentValueOfCoupon_Annuity()
    expected_pv_coupons = coupon * b.PVIFA(N)
    assert math.isclose(pv_coupons, expected_pv_coupons)

    # Full price equals PV of coupons plus PV of par
    expected_price = expected_pv_coupons + b.PresentValueOfPar()
    assert math.isclose(b.Price(), expected_price)


def test_present_value_generic():
    b = Bullet(1000, "2026-01-01", "2024-01-01", 0.10, annual_compound=1)
    fv = 1210
    periods = b.TotalPeriods()
    pv = b.PresentValue(fv, periods)
    expected = fv * (1 / ((1 + b.Rate()) ** periods))
    assert math.isclose(pv, expected)


def test_abstract_methods_raise():
    vb = VanillaBond(1000, "2026-01-01", "2024-01-01", 0.05)
    with pytest.raises(Exception):
        vb.Rate()
    with pytest.raises(Exception):
        vb.FutureValue(1)
    with pytest.raises(Exception):
        vb.Price()

