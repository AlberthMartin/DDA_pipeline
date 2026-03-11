import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from scipy.integrate import cumulative_trapezoid
from pathlib import Path

from validation import validate_dataframe
from metadata import generate_metadata, save_metadata
from logger import logger


# Heat release parameters
V = 0.0065
GAMMA = 1.325

# Pressure filter
PRESSURE_CUTOFF = 700
PRESSURE_ORDER = 4

# HRR filter
HRR_CUTOFF = 500
HRR_ORDER = 5


def run_stage2(input_folder, output_folder, metadata_dir, stats):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    metadata_dir = Path(metadata_dir)

    output_folder.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    files = list(input_folder.glob("*.csv"))
    logger.info(f"Stage2 started: found {len(files)} bronze files")

    for file in files:
        logger.info(f"Processing {file.name}")

        df = pd.read_csv(file)
        df = validate_dataframe(df)

        required = ["Time_s", "ChamberPressure_BarA_", "MainInjector_CurrentProfile"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"{file.name} is missing required columns: {missing}")

        t = df["Time_s"].to_numpy()
        p_bar = df["ChamberPressure_BarA_"].to_numpy()

        # ensure sorted by time
        if np.any(np.diff(t) <= 0):
            order = np.argsort(t)
            df = df.iloc[order].reset_index(drop=True)
            t = df["Time_s"].to_numpy()
            p_bar = df["ChamberPressure_BarA_"].to_numpy()

        dt = np.median(np.diff(t))
        if not np.isfinite(dt) or dt <= 0:
            raise ValueError(f"{file.name} has invalid time vector")

        Fs = 1.0 / dt

        # pressure in Pa
        p_pa = p_bar * 1e5
        p_pa = pd.Series(p_pa).interpolate().bfill().ffill().to_numpy()

        # filtered pressure
        wn_p = PRESSURE_CUTOFF / (Fs / 2)
        if wn_p >= 1:
            raise ValueError(
                f"{file.name}: pressure cutoff too high for Fs={Fs:.1f} Hz"
            )

        b_p, a_p = butter(PRESSURE_ORDER, wn_p, btype="low")
        p_filt_pa = filtfilt(b_p, a_p, p_pa)

        # derivative
        dpdt = np.gradient(p_filt_pa, t)

        # heat release rate in W
        hrr_w = (V / (GAMMA - 1.0)) * dpdt

        # smooth HRR
        wn_h = HRR_CUTOFF / (Fs / 2)
        if wn_h >= 1:
            raise ValueError(
                f"{file.name}: HRR cutoff too high for Fs={Fs:.1f} Hz"
            )

        b_h, a_h = butter(HRR_ORDER, wn_h, btype="low")
        hrr_w_filt = filtfilt(b_h, a_h, hrr_w)

        # convert to kW
        hrr_kw = hrr_w_filt / 1000.0

        # cumulative heat release in J
        cumulative_hr_j = cumulative_trapezoid(hrr_kw, t, initial=0) * 1000.0

        # shift cumulative heat so value at t=0 is zero
        i0 = int(np.argmin(np.abs(t)))
        cumulative_hr_j = cumulative_hr_j - cumulative_hr_j[i0]

        # save derived columns
        df["ChamberPressure_BarA_ButterFilter"] = p_filt_pa / 1e5
        df["Derivate_filtered_pressure"] = dpdt
        df["HeatRelease_ButterFilter"] = hrr_kw
        df["CumulativeHeatRelease_ButterFilter"] = cumulative_hr_j

        out_file = output_folder / file.name
        df.to_csv(out_file, index=False)

        metadata = generate_metadata(df, file.name)
        metadata["sampling_frequency_hz"] = float(Fs)
        save_metadata(metadata, metadata_dir / f"{file.stem}.json")

        stats.file_done()
        logger.info(f"Finished {file.name} -> {out_file}")