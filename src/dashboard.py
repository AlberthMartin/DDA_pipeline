#import streamlit as st
#import pandas as pd
#from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parent.parent

#GOLD = BASE_DIR / "data" / "gold"

#st.title("Combustion Data Dashboard")

#files = list(Path(GOLD).glob("*.csv"))

#choice = st.selectbox("Select testpoint", files)

#df = pd.read_csv(choice)

#st.line_chart(df["ChamberPressure_BarA_ButterFilter_mean"])

#st.line_chart(df["HeatRelease_ButterFilter_mean"])

#st.line_chart(df["CumulativeHeatRelease_ButterFilter_mean"])

#st.line_chart(df["MainInjector_CurrentProfile_mean"])

import streamlit as st
import pandas as pd
from pathlib import Path
import json
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

GOLD = BASE_DIR / "data" / "gold"
STATS = BASE_DIR / "data" / "stats" / "pipeline_stats.json"

st.set_page_config(page_title="Combustion Data Dashboard", layout="wide")

st.title("Combustion Data Pipeline Dashboard")

gold_folder = Path(GOLD)
stats_file = Path(STATS)

files = list(gold_folder.glob("*.csv"))

if not files:
    st.warning("No processed data found.")
    st.stop()

# Testpoint selection
file = st.selectbox("Select Testpoint", files)

df = pd.read_csv(file)

t = df["Time_s"] * 1000

# Plot
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

# Pipeline statistics
st.header("Pipeline Statistics")

if stats_file.exists():

    stats = json.load(open(stats_file))

    st.json(stats)

# Metadata
st.header("Metadata")

metadata_folder = Path("data/metadata")

meta_file = metadata_folder / f"{file.stem}.json"

if meta_file.exists():

    metadata = json.load(open(meta_file))

    st.json(metadata)