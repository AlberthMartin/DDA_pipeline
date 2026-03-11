import pandas as pd
from pathlib import Path


def test_required_columns_in_bronze():
    sample = next(Path("data/bronze").glob("*.csv"), None)
    assert sample is not None, "No bronze files found"

    df = pd.read_csv(sample)

    required = [
        "Time_s",
        "ChamberPressure_BarA_",
        "MainInjector_CurrentProfile"
    ]

    for col in required:
        assert col in df.columns, f"Missing {col} in bronze file"


def test_gold_outputs_exist():
    gold_files = [f for f in Path("data/gold").glob("*.csv") if "_avg_" in f.stem or f.stem.endswith("_avg")]
    assert len(gold_files) > 0, "No averaged gold outputs created"


def test_gold_pressure_columns_exist():
    file = next((f for f in Path("data/gold").glob("*.csv") if "_avg_" in f.stem or f.stem.endswith("_avg")), None)
    assert file is not None, "No averaged gold file found"

    df = pd.read_csv(file)

    assert "ChamberPressure_BarA_ButterFilter_mean" in df.columns
    assert "ChamberPressure_BarA_ButterFilter_std" in df.columns