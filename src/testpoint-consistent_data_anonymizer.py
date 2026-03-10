import pandas as pd
import numpy as np
from pathlib import Path
import re

# -----------------------------
# SETTINGS
# -----------------------------

INPUT_FOLDER = "/Users/alberthmartin/Desktop/DDA_pipeline_data"
OUTPUT_FOLDER = "/Users/alberthmartin/Desktop/DDA_anonymized_data"

np.random.seed(42)

REMOVE_COLUMNS = [
    "HeatRelease",
    "ChamberPressure_BarA__FIRFilter_Derivative",
    "ChamberPressure_BarA__FIRFilter",
    "MainInjector_CurrentProfile_FIRFilter",
    "IntakePressure_FIRFilter",
    "Backpressure_FIRFilter"
]

KEEP_COLUMNS = [
    "Time_s",
    "MainInjector_CurrentProfile"
]

MODIFY_COLUMNS = [
    "ControlOilToInjector",
    "ChamberPressure_BarA_",
    "TemperatureAcc_IdealGasLaw",
    "Backpressure",
    "ChamberGasTemperature",
    "IntakePressure",
    "FuelPressure"
]

# Realistic new ranges (can adjust)
TARGET_RANGES = {

    "ControlOilToInjector": (20, 80),
    "ChamberPressure_BarA_": (10, 120),
    "TemperatureAcc_IdealGasLaw": (600, 2600),
    "Backpressure": (1, 6),
    "ChamberGasTemperature": (700, 2700),
    "IntakePressure": (0.8, 3),
    "FuelPressure": (300, 2000)
}


def get_testpoint(filename):
    m = re.match(r"(T\d+)_", filename)
    return m.group(1) if m else None


def create_transform():

    return {
        "curve_warp": np.random.uniform(0.8, 1.2),
        "noise": np.random.uniform(0.01, 0.03)
    }


def transform_signal(signal, target_range, transform):

    s = signal.copy()

    # Normalize shape
    s = (s - s.min()) / (s.max() - s.min() + 1e-9)

    # Nonlinear curve warp
    s = s ** transform["curve_warp"]

    # Add small noise
    noise_level = transform["noise"]
    s = s + np.random.normal(0, noise_level, size=len(s))

    # Re-normalize
    s = (s - s.min()) / (s.max() - s.min() + 1e-9)

    # Rescale to target physical range
    low, high = target_range
    s = s * (high - low) + low

    return s


def main():

    input_path = Path(INPUT_FOLDER)
    output_path = Path(OUTPUT_FOLDER)

    output_path.mkdir(exist_ok=True)

    files = list(input_path.glob("*.csv"))

    groups = {}

    for f in files:
        tp = get_testpoint(f.name)
        if tp:
            groups.setdefault(tp, []).append(f)

    print(f"Detected {len(groups)} testpoints")

    for tp, flist in groups.items():

        print(f"Processing {tp}")

        transforms = {}

        for col in MODIFY_COLUMNS:
            transforms[col] = create_transform()

        for file in flist:

            df = pd.read_csv(file)

            df = df.drop(columns=[c for c in REMOVE_COLUMNS if c in df.columns])

            for col in MODIFY_COLUMNS:

                if col not in df.columns:
                    continue

                df[col] = transform_signal(
                    df[col].values,
                    TARGET_RANGES[col],
                    transforms[col]
                )

            out_file = output_path / file.name

            df.to_csv(out_file, index=False)

    print("Finished anonymizing data.")


if __name__ == "__main__":
    main()