from fastapi import FastAPI
import pandas as pd
from pathlib import Path
import json

app = FastAPI(title="Combustion Data API")

BASE_DIR = Path(__file__).resolve().parent.parent

GOLD = BASE_DIR / "data" / "gold"
STATS = BASE_DIR / "data" / "stats" / "pipeline_stats.json"

gold_folder = Path(GOLD)
stats_file = Path(STATS)


@app.get("/")
def root():

    return {"message": "Combustion Data Pipeline API"}


@app.get("/testpoints")
def get_testpoints():

    files = list(gold_folder.glob("*.csv"))

    return [f.stem for f in files]


@app.get("/pressure/{testpoint}")
def get_pressure(testpoint: str):

    file = gold_folder / f"{testpoint}.csv"

    if not file.exists():
        return {"error": "Testpoint not found"}

    df = pd.read_csv(file)

    return df.to_dict(orient="list")


@app.get("/stats")
def get_stats():

    if stats_file.exists():

        return json.load(open(stats_file))

    return {"error": "No stats found"}