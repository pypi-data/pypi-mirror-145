from unicef_business_areas.models import BusinessArea, Region


def test_region():
    reg = Region(name="test_name")
    assert str(reg) == 'test_name'


def test_business_area():
    ab = BusinessArea(name="test_name")
    assert str(ab) == 'test_name'
