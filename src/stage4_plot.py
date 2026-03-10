import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def run_stage4(avg_folder, rep_folder, plot_folder):

    avg_folder = Path(avg_folder)
    rep_folder = Path(rep_folder)
    plot_folder = Path(plot_folder)

    plot_folder.mkdir(parents=True, exist_ok=True)

    avg_files = list(avg_folder.glob("*.csv"))

    for avg_file in avg_files:

        tp = avg_file.stem.split("_")[0]

        reps = list(rep_folder.glob(f"*{tp}*.csv"))

        A = pd.read_csv(avg_file)

        t = A["Time_s"] * 1000

        # Mean/std signals
        pMean = A["ChamberPressure_BarA_ButterFilter_mean"]
        pStd = A["ChamberPressure_BarA_ButterFilter_std"]

        hMean = A["HeatRelease_ButterFilter_mean"]
        hStd = A["HeatRelease_ButterFilter_std"]

        cMean = A["CumulativeHeatRelease_ButterFilter_mean"]
        cStd = A["CumulativeHeatRelease_ButterFilter_std"]

        iMean = A["MainInjector_CurrentProfile_mean"]
        iStd = A["MainInjector_CurrentProfile_std"]

        # Create plots
        fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

        # --------------------------------------------------
        # Injector current
        # --------------------------------------------------

        for rep in reps:
            df = pd.read_csv(rep)

            axs[0].plot(
                df["Time_s"] * 1000,
                df["MainInjector_CurrentProfile"],
                color="lightgray",
                linewidth=1
            )

        axs[0].plot(t, iMean, linewidth=2)
        axs[0].fill_between(t, iMean - iStd, iMean + iStd, alpha=0.2)

        axs[0].axvline(0, linestyle="--", linewidth=1)  # SoE marker
        axs[0].set_title(f"{tp} Injector Current")
        axs[0].set_ylabel("Current")

        # --------------------------------------------------
        # Pressure
        # --------------------------------------------------

        for rep in reps:
            df = pd.read_csv(rep)

            axs[1].plot(
                df["Time_s"] * 1000,
                df["ChamberPressure_BarA_ButterFilter"],
                color="lightgray",
                linewidth=1
            )

        axs[1].plot(t, pMean, linewidth=2)
        axs[1].fill_between(t, pMean - pStd, pMean + pStd, alpha=0.2)

        axs[1].axvline(0, linestyle="--", linewidth=1)
        axs[1].set_title("Chamber Pressure")
        axs[1].set_ylabel("Bar")

        # --------------------------------------------------
        # Heat release rate
        # --------------------------------------------------

        for rep in reps:
            df = pd.read_csv(rep)

            axs[2].plot(
                df["Time_s"] * 1000,
                df["HeatRelease_ButterFilter"],
                color="lightgray",
                linewidth=1
            )

        axs[2].plot(t, hMean, linewidth=2)
        axs[2].fill_between(t, hMean - hStd, hMean + hStd, alpha=0.2)

        axs[2].axvline(0, linestyle="--", linewidth=1)
        axs[2].set_title("Heat Release Rate")
        axs[2].set_ylabel("kW")

        # --------------------------------------------------
        # Cumulative heat release
        # --------------------------------------------------

        for rep in reps:
            df = pd.read_csv(rep)

            axs[3].plot(
                df["Time_s"] * 1000,
                df["CumulativeHeatRelease_ButterFilter"],
                color="lightgray",
                linewidth=1
            )

        axs[3].plot(t, cMean, linewidth=2)
        axs[3].fill_between(t, cMean - cStd, cMean + cStd, alpha=0.2)

        axs[3].axvline(0, linestyle="--", linewidth=1)
        axs[3].set_title("Cumulative Heat Release")
        axs[3].set_ylabel("J")
        axs[3].set_xlabel("Time [ms]")

        plt.tight_layout()

        outfile = plot_folder / f"{tp}_verify.png"

        plt.savefig(outfile, dpi=200)
        plt.close()