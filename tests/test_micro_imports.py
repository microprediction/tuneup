from microconventions import MicroConventions
from microconventions.stats_conventions import StatsConventions

from tuneup.nothing import chickens

def test_chickens():
    assert "bock" in chickens()