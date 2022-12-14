from os import system
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/load_data/data", methods=["GET"])
def load_data_data():
    z = ZipFile("DATASETS/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    return data.to_json(orient='values')

@app.route("/load_data/sample", methods=["GET"])
def load_data_sample():
    z = ZipFile("DATASETS/X_enc.zip")
    sample = pd.read_csv(z.open('X_enc.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    return sample.to_json(orient='values')

@app.route("/load_data/description", methods=["GET"])
def load_data_description():
    description = pd.read_csv("DATASETS/features_description.csv",
                              usecols=['Row', 'Description'], index_col=0, encoding='unicode_escape')
    return description.to_json(orient='values')

@app.route("/load_data/target", methods=["GET"])
def load_data_target():
    z = ZipFile("DATASETS/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    target = data.iloc[:, -1:]
    return json.dumps(list(target))

@app.route("/load_infos_gen/credit", methods=["GET"])
def load_infos_gen_credit():
    z = ZipFile("DATASETS/data_final.zip")
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
    z = ZipFile("DATASETS/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    targets = data.TARGET.value_counts()
    return json.dumps(list(targets))

@app.route("/load_age_population", methods=["GET"])
def load_age_population():
    z = ZipFile("DATASETS/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    data_age = round((data["DAYS_BIRTH"]/365), 2)
    return json.dumps(list(data_age))

@app.route("/load_income_population", methods=["GET"])
def load_income_population():
    z = ZipFile("DATASETS/X_enc.zip")
    sample = pd.read_csv(z.open('X_enc.csv'), index_col='SK_ID_CURR', encoding='utf-8')
    df_income = pd.DataFrame(sample["AMT_INCOME_TOTAL"])
    df_income = df_income.loc[df_income['AMT_INCOME_TOTAL'] < 200000, :]
    return df_income.to_json(orient='values')

if __name__ == "__main__":
    app.run(host="localhost", port="3999", debug=True)
