from pathlib import Path
import time

from stage2_add_filtered_columns import run_stage2
from stage3_average import run_stage3
from stage4_plot import run_stage4
from stats import PipelineStats
#from model import train_model

BASE_DIR = Path(__file__).resolve().parent.parent

BRONZE = BASE_DIR / "data" / "bronze"
SILVER = BASE_DIR / "data" / "silver"
GOLD = BASE_DIR / "data" / "gold"
PLOTS = BASE_DIR / "data" / "plots"
METADATA = BASE_DIR / "data" / "metadata"
STATS = BASE_DIR / "data" / "stats"

def main():

    stats = PipelineStats()

    run_stage2(BRONZE,SILVER,METADATA, stats)
    run_stage3(SILVER,GOLD)
    run_stage4(GOLD, SILVER, PLOTS)

    #train_model(GOLD)

    stats.save(STATS/"pipeline_stats.json")


if __name__ == "__main__":
    # Automatic ingestion if files added
    while True:
        main()
        print("Pipeline completed, waiting for new files...")
        time.sleep(300)