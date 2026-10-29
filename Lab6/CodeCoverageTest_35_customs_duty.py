import pytest
from customs_duty import duty_rate, total_duty, clearance_channel

def test_duty_rate_all_lines():
    assert duty_rate("electronics", "FTA") == 0.10
    assert duty_rate("electronics", "US") == 0.20
    assert duty_rate("clothing", "FTA") == 0.05
    assert duty_rate("clothing", "US") == 0.12
    assert duty_rate("books", "US") == 0
    assert duty_rate("other", "US") == 0.15
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("weapons", "US")

def test_total_duty_all_lines():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("books", -10, "US", False)
    
    # Gift tests
    assert total_duty("books", 4000, "US", True) == 0
    assert total_duty("clothing", 5100, "FTA", True) == 50  # triggers 0 < duty < 50 rule
    assert total_duty("electronics", 10000, "US", True) == 1000

    # Non-gift tests
    assert total_duty("books", 800, "US", False) == 0
    assert total_duty("electronics", 2000, "US", False) == 400

def test_clearance_channel_all_lines():
    assert clearance_channel(500, "weapons", True) == "refuse"
    assert clearance_channel(150000, "electronics", True) == "inspect"
    assert clearance_channel(30000, "electronics", False) == "inspect"
    assert clearance_channel(500, "electronics", True) == "green"