import streamlit as st
import pandas as pd
from pathlib import Path
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="Combustion Data Dashboard", layout="wide")
st.title("Combustion Data Pipeline Dashboard")

gold_folder = Path("data/gold")
stats_file = Path("data/stats/pipeline_stats.json")

files = [f for f in gold_folder.glob("*.csv") if "_avg_" in f.stem or f.stem.endswith("_avg")]

if not files:
    st.warning("No processed gold data found.")
    st.stop()

file = st.selectbox("Select Testpoint", files)
df = pd.read_csv(file)

required = [
    "Time_s",
    "ChamberPressure_BarA_ButterFilter_mean",
    "ChamberPressure_BarA_ButterFilter_std"
]

missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing columns in selected file: {missing}")
    st.stop()

t = df["Time_s"] * 1000

fig, ax = plt.subplots()

ax.plot(t, df["ChamberPressure_BarA_ButterFilter_mean"], label="Mean Pressure")
ax.fill_between(
    t,
    df["ChamberPressure_BarA_ButterFilter_mean"] - df["ChamberPressure_BarA_ButterFilter_std"],
    df["ChamberPressure_BarA_ButterFilter_mean"] + df["ChamberPressure_BarA_ButterFilter_std"],
    alpha=0.3,
    label="Std"
)
ax.axvline(0, linestyle="--", label="SoE")
ax.set_xlabel("Time [ms]")
ax.set_ylabel("Pressure [bar]")
ax.set_title(file.stem)
ax.legend()

st.pyplot(fig)

st.header("Pipeline Statistics")
if stats_file.exists():
    stats = json.load(open(stats_file))
    st.json(stats)

st.header("Columns")
st.write(list(df.columns))

st.header("Preview")
st.dataframe(df.head())