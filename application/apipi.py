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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import re
import os

plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')

app = Flask(__name__)

def load_data():
    z = ZipFile("data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding ='utf-8')
    z = ZipFile("data/X_enc.zip")
    sample = pd.read_csv(z.open('X_enc.csv'), index_col='SK_ID_CURR', encoding ='utf-8')
    description = pd.read_csv("data/features_description.csv",
                                  usecols=['Row', 'Description'], index_col=0, encoding= 'unicode_escape')
    target = data.iloc[:, -1:]

    return data, sample, target, description

@app.route("/load_infos_gen/credit", methods=["GET"])
def load_infos_gen_credit():
    z = ZipFile("data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    lst_infos = [data.shape[0],
                 round(data["AMT_INCOME_TOTAL"].mean(), 2),
                 round(data["AMT_CREDIT"].mean(), 2)]
    nb_credits = lst_infos[0]
    rev_moy = lst_infos[1]
    credits_moy = lst_infos[2]
    return jsonify(nb_credits, rev_moy, credits_moy)

@app.route("/load_infos_gen/targets", methods=["GET"])
def load_infos_gen_targets():
    z = ZipFile("data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    targets = data.TARGET.value_counts()
    return json.dumps(list(targets))

@app.route("/load_age_population", methods=["GET"])
def load_age_population():
    z = ZipFile("data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    data_age = round((data["DAYS_BIRTH"]/365), 2)
    return json.dumps(list(data_age))

@app.route("/load_income_population", methods=["GET"])
def load_income_population():
    z = ZipFile("data/X_enc.zip")
    sample = pd.read_csv(z.open('X_enc.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    df_income = pd.DataFrame(sample["AMT_INCOME_TOTAL"])
    df_income = df_income.loc[df_income['AMT_INCOME_TOTAL'] < 200000, :]
    return df_income.to_json(orient='values')

if __name__ == "__main__":
    app.run(host="localhost", port="4001", debug=True)