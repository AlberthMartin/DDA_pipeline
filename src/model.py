import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
import joblib


def train_model(gold_folder):

    gold_folder = Path(gold_folder)

    data = []

    for f in gold_folder.glob("*.csv"):
        if "_avg_" not in f.stem and not f.stem.endswith("_avg"):
            continue

        df = pd.read_csv(f)

        if "ChamberPressure_BarA_ButterFilter_mean" not in df.columns:
            continue

        peak_pressure = df["ChamberPressure_BarA_ButterFilter_mean"].max()
        peak_hrr = df["HeatRelease_ButterFilter_mean"].max() if "HeatRelease_ButterFilter_mean" in df.columns else None

        data.append({
            "testpoint": f.stem,
            "peak_pressure": peak_pressure,
            "peak_hrr": peak_hrr
        })

    if len(data) < 2:
        print("Not enough gold files to train ML model.")
        return None

    dataset = pd.DataFrame(data)

    X = dataset.index.values.reshape(-1, 1)
    y = dataset["peak_pressure"]

    model = LinearRegression()
    model.fit(X, y)

    model_path = gold_folder / "linear_model_peak_pressure.pkl"
    joblib.dump(model, model_path)

    print(f"Saved ML model to {model_path}")
    return model