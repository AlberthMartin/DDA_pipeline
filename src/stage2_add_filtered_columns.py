import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from scipy.integrate import cumulative_trapezoid
from pathlib import Path
from tqdm import tqdm

V = 0.0065
gamma = 1.325

FCUT_PRESSURE = 700
FCUT_HRR = 500

ORDER_P = 3
ORDER_H = 5


def run_stage2(input_folder, output_folder):

    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    files = list(input_folder.glob("*.csv"))

    print(f"Processing {len(files)} CSV files")

    for file in tqdm(files):

        df = pd.read_csv(file)

        t = df["Time_s"].values
        p_bar = df["ChamberPressure_BarA_"].values

        dt = np.median(np.diff(t))
        Fs = 1 / dt

        p_pa = p_bar * 1e5
        p_pa = pd.Series(p_pa).interpolate().bfill().ffill().values

        b, a = butter(ORDER_P, FCUT_PRESSURE/(Fs/2), btype="low")
        p_filt = filtfilt(b, a, p_pa)

        dpdt = np.gradient(p_filt, t)

        HRR_W = (V/(gamma-1)) * dpdt

        b2, a2 = butter(ORDER_H, FCUT_HRR/(Fs/2), btype="low")
        HRR_filt = filtfilt(b2, a2, HRR_W)

        HRR_kW = HRR_filt / 1000

        cumHR = cumulative_trapezoid(HRR_kW, t, initial=0) * 1000

        df["ChamberPressure_BarA_ButterFilter"] = p_filt / 1e5
        df["Derivate_filtered_pressure"] = dpdt
        df["HeatRelease_ButterFilter"] = HRR_kW
        df["CumulativeHeatRelease_ButterFilter"] = cumHR

        out_file = output_folder / file.name
        df.to_csv(out_file, index=False)