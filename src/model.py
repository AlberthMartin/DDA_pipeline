""" import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model(gold_folder):

    data = []

    for f in gold_folder.glob("*.csv"):
        df = pd.read_csv(f)

        peak = df["Pressure_mean"].max()

        data.append({"testpoint":f.stem,"peak_pressure":peak})

    dataset = pd.DataFrame(data)

    X = dataset.index.values.reshape(-1,1)
    y = dataset["ChamberPressure_BarA_ButterFilter_mean"]

    model = LinearRegression()
    model.fit(X,y)

    return model

""" 