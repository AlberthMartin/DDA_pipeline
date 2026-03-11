from fastapi import FastAPI
import pandas as pd
from pathlib import Path
import json

app = FastAPI(title="Combustion Data API")

gold_folder = Path("data/gold")
stats_file = Path("data/stats/pipeline_stats.json")


@app.get("/")
def root():
    return {"message": "Combustion Data Pipeline API"}


@app.get("/testpoints")
def get_testpoints():
    files = [f for f in gold_folder.glob("*.csv") if "_avg_" in f.stem or f.stem.endswith("_avg")]
    return [f.stem for f in files]


@app.get("/pressure/{testpoint}")
def get_pressure(testpoint: str):
    file = gold_folder / f"{testpoint}.csv"

    if not file.exists():
        return {"error": "Testpoint not found"}

    df = pd.read_csv(file)

    required = [
        "Time_s",
        "ChamberPressure_BarA_ButterFilter_mean",
        "ChamberPressure_BarA_ButterFilter_std"
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        return {"error": f"Missing columns: {missing}"}

    return {
        "Time_s": df["Time_s"].tolist(),
        "Pressure_mean": df["ChamberPressure_BarA_ButterFilter_mean"].tolist(),
        "Pressure_std": df["ChamberPressure_BarA_ButterFilter_std"].tolist(),
    }


@app.get("/stats")
def get_stats():
    if stats_file.exists():
        return json.load(open(stats_file))
    return {"error": "No stats found"}