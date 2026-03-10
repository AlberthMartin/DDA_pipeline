import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import re


def run_stage3(input_folder, output_folder):

    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    files = list(input_folder.glob("*.csv"))

    pattern = re.compile(r"(T\d+).*?(\d{4})")

    groups = {}

    for f in files:

        m = pattern.search(f.stem)

        if not m:
            continue

        tp = m.group(1)

        groups.setdefault(tp, []).append(f)

    for tp, flist in groups.items():

        print(f"{tp} -> {len(flist)} repetitions")

        mats = []

        for f in flist:

            df = pd.read_csv(f)

            mats.append(df)

        t = mats[0]["Time_s"]

        P = np.stack([d["ChamberPressure_BarA_ButterFilter"] for d in mats], axis=1)
        H = np.stack([d["HeatRelease_ButterFilter"] for d in mats], axis=1)
        C = np.stack([d["CumulativeHeatRelease_ButterFilter"] for d in mats], axis=1)
        I = np.stack([d["MainInjector_CurrentProfile"] for d in mats], axis=1)

        out = pd.DataFrame()

        out["Time_s"] = t

        out["ChamberPressure_BarA_ButterFilter_mean"] = P.mean(axis=1)
        out["ChamberPressure_BarA_ButterFilter_std"] = P.std(axis=1)

        out["HeatRelease_ButterFilter_mean"] = H.mean(axis=1)
        out["HeatRelease_ButterFilter_std"] = H.std(axis=1)

        out["CumulativeHeatRelease_ButterFilter_mean"] = C.mean(axis=1)
        out["CumulativeHeatRelease_ButterFilter_std"] = C.std(axis=1)

        out["MainInjector_CurrentProfile_mean"] = I.mean(axis=1)
        out["MainInjector_CurrentProfile_std"] = I.std(axis=1)

        outfile = output_folder / f"{tp}_avg_{len(flist)}reps.csv"

        out.to_csv(outfile, index=False)