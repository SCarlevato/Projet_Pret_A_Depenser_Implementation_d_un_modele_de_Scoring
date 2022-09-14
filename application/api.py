import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import shap
import plotly.express as px
from zipfile import ZipFile
from sklearn.cluster import KMeans
plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')

app = Flask(__name__)

@app.route("/load_data/data", methods=["GET"])
def load_data_data():
    z = ZipFile("/Users/sylvaincarlevato/p7scoringopenclassrooms/data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    return data.to_json(orient='values')

@app.route("/load_data/sample", methods=["GET"])
def load_data_sample():
    z = ZipFile("/Users/sylvaincarlevato/p7scoringopenclassrooms/data/X_enc.zip")
    sample = pd.read_csv(z.open('X_enc.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    return sample.to_json(orient='values')

@app.route("/load_data/description", methods=["GET"])
def load_data_description():
    description = pd.read_csv("/Users/sylvaincarlevato/p7scoringopenclassrooms/data/features_description.csv",
                              usecols=['Row', 'Description'], index_col=0, encoding='unicode_escape')
    return description.to_json(orient='values')

@app.route("/load_data/target", methods=["GET"])
def load_data_target():
    z = ZipFile("/Users/sylvaincarlevato/p7scoringopenclassrooms/data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    target = data.iloc[:, -1:]
    return json.dumps(list(target))

if __name__ == "__main__":
    app.run(host="localhost", port="4001", debug=True)
