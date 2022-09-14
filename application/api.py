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

@app.route("/load_age_population", methods=["GET"])

def load_age_population():

    z = ZipFile("/Users/sylvaincarlevato/p7scoringopenclassrooms/data/data_final.zip")

    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')

    data_age = round((data["DAYS_BIRTH"]/365), 2)

    return json.dumps(list(data_age))


 



if __name__ == "__main__":
    app.run(host="localhost", port="4001", debug=True)
