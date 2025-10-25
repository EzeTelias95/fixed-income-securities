import pytest

from fixed-income-securities.models.DaysConvention import (
    DaysConvention,
    GovStandard,
    MarketStandard,
)


def test_days_convention_base_instantiation():
    dc = DaysConvention()
    assert isinstance(dc, DaysConvention)


@pytest.mark.parametrize("cls", [GovStandard, MarketStandard])
def test_subclasses_inherit_days_convention(cls):
    inst = cls()
    assert isinstance(inst, DaysConvention)
    assert isinstance(inst, cls)

