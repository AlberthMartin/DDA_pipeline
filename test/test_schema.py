import pandas as pd
from pathlib import Path


def test_required_columns():

    sample = Path("data/bronze").glob("*.csv")

    file = next(sample, None)

    assert file is not None, "No bronze files found"

    df = pd.read_csv(file)

    required = [
        "Time_s",
        "ChamberPressure_BarA_",
        "MainInjector_CurrentProfile"
    ]

    for col in required:
        assert col in df.columns


def test_gold_outputs():

    gold_files = list(Path("data/gold").glob("*.csv"))

    assert len(gold_files) > 0, "No gold outputs created"


def test_pressure_values():

    file = next(Path("data/gold").glob("*.csv"), None)

    assert file is not None

    df = pd.read_csv(file)

    assert df["Pressure_mean"].max() > 0