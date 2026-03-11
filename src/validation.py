REQUIRED_COLUMNS = [
    "Time_s",
    "ChamberPressure_BarA_",
    "MainInjector_CurrentProfile"
]

def validate_dataframe(df):

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column {col}")

    df = df.interpolate().bfill().ffill()

    return df