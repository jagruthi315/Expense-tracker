import pandas as pd
from pathlib import Path
from src.ingest import read_bank_csv

def test_read_bank_csv_columns():
    sample_path = Path(__file__).parent /"sample.csv"
    df = read_bank_csv(sample_path, account="Test")
    assert not df.empty

    assert "tx_date" in df.columns
    assert "description" in df.columns
    assert "amount" in df.columns
    assert "account" in df.columns
