from pathlib import Path

from stage2_filter import run_stage2
from stage3_average import run_stage3
from stage4_plot import run_stage4
from stats import PipelineStats
from model import train_model


BASE_DIR = Path(__file__).resolve().parent.parent

BRONZE = BASE_DIR / "data" / "bronze"
SILVER = BASE_DIR / "data" / "silver"
GOLD = BASE_DIR / "data" / "gold"
PLOTS = BASE_DIR / "data" / "plots"
METADATA = BASE_DIR / "data" / "metadata"
STATS_DIR = BASE_DIR / "data" / "stats"


def main():
    SILVER.mkdir(parents=True, exist_ok=True)
    GOLD.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)
    STATS_DIR.mkdir(parents=True, exist_ok=True)

    stats = PipelineStats()

    print("Stage 2: Data Validation & Signal Processing (Bronze → Silver)")
    run_stage2(BRONZE, SILVER, METADATA, stats)

    print("Stage 3: Testpoint Aggregation (Silver → Gold)")
    run_stage3(SILVER, GOLD)

    print("Stage 4: Data Product Generation (Visualization)")
    run_stage4(GOLD, SILVER, PLOTS)

    print("Stage 5: Predictive Analytics (ML Model Training)")
    train_model(GOLD)

    stats.save(STATS_DIR / "pipeline_stats.json")


if __name__ == "__main__":
    main()