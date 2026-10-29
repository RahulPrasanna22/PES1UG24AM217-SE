import pytest
from customs_duty import duty_rate, total_duty, clearance_channel

def test_duty_rate_branches():
    assert duty_rate("electronics", "FTA") == 0.10
    assert duty_rate("electronics", "US") == 0.20
    assert duty_rate("clothing", "FTA") == 0.05
    assert duty_rate("clothing", "US") == 0.12
    assert duty_rate("books", "US") == 0
    assert duty_rate("other", "US") == 0.15
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("narcotics", "US")

def test_total_duty_branches():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -100, "US", False)
    
    assert total_duty("electronics", 4000, "US", True) == 0
    assert total_duty("clothing", 5100, "FTA", True) == 50
    assert total_duty("electronics", 10000, "US", True) == 1000
    
    assert total_duty("books", 1000, "US", False) == 0
    assert total_duty("electronics", 2000, "US", False) == 400

def test_clearance_channel_branches():
    # Covers all True/False branch evaluations
    assert clearance_channel(100, "weapons", True) == "refuse"
    assert clearance_channel(200000, "electronics", True) == "inspect"
    assert clearance_channel(30000, "electronics", False) == "inspect"
    assert clearance_channel(30000, "electronics", True) == "green"
    assert clearance_channel(500, "electronics", True) == "green"