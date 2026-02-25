from src.categorize import categorize_transaction

def test_food_category():
    category = categorize_transaction("Swiggy order")
    assert category == "Food"

def test_transport_category():
    category = categorize_transaction("Uber ride")
    assert category == "Transport"
