from pathlib import Path

from stage2_add_filtered_columns import run_stage2
from stage3_average import run_stage3
from stage4_plot import run_stage4


BASE_DIR = Path(__file__).resolve().parent.parent

BRONZE = BASE_DIR / "data" / "bronze"
SILVER = BASE_DIR / "data" / "silver"
GOLD = BASE_DIR / "data" / "gold"
PLOTS = BASE_DIR / "data" / "plots"


def main():

    print("Stage 2: Filtering")
    run_stage2(BRONZE, SILVER)

    print("Stage 3: Averaging")
    run_stage3(SILVER, GOLD)

    print("Stage 4: Plotting")
    run_stage4(GOLD, SILVER, PLOTS)


if __name__ == "__main__":
    main()