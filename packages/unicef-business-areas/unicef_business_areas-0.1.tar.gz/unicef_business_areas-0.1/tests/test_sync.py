from pathlib import Path

from unicef_business_areas.sync import load_business_area, load_region

from .vcrpy import VCR


@VCR.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/load_business_area.yml'))
def test_load_business_area(db):
    ret = load_business_area()
    assert len(ret.created) == 161
    assert len(ret.updated) == 0


@VCR.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/load_region.yml'))
def test_load_region(db):
    ret = load_region()
    assert len(ret.created) == 8
    assert len(ret.updated) == 0
