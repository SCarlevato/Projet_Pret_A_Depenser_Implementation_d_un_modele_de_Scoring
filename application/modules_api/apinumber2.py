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
import requests
import json
from PIL import Image

plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')

def load_data():
    z = ZipFile("data/data_final.zip")
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding ='utf-8'
    z = ZipFile("data/X_enc.zip")
    sample = pd.read_csv(z.open('X_enc.csv'), index_col='SK_ID_CURR', encoding ='utf-8')
    description = pd.read_csv("data/features_description.csv", usecols=['Row', 'Description'], index_col=0, encoding= 'unicode_escape')
    target = data.iloc[:, -1:]
    return data, sample, target, description

def load_model():
    '''Chargement du Modèle Entraîné'''
    pickle_in = open('modele/classifier_xgb_model.pkl', 'rb')
    clf = pickle.load(pickle_in)
    return clf
                       
def load_knn(sample):
     knn = knn_training(sample)
     return knn

def load_infos_gen(data):
    lst_infos = [data.shape[0],
                     round(data["AMT_INCOME_TOTAL"].mean(), 2),
                     round(data["AMT_CREDIT"].mean(), 2)]

     nb_credits = lst_infos[0]
     rev_moy = lst_infos[1]
     credits_moy = lst_infos[2]
     targets = data.TARGET.value_counts()
     return nb_credits, rev_moy, credits_moy, targets

def identite_client(data, id):
     data_client = data[data.index == int(id)]
     return data_client

def load_age_population(data):
     data_age = round((data["DAYS_BIRTH"]/365), 2)
     return data_age

def load_income_population(sample):
     df_income = pd.DataFrame(sample["AMT_INCOME_TOTAL"])
     df_income = df_income.loc[df_income['AMT_INCOME_TOTAL'] < 200000, :]
     return df_income

def load_prediction(sample, id, clf):
     X=sample.iloc[:, :-1]
     score = clf.predict_proba(X[X.index == int(id)])[:,1]
     return score

 def load_kmeans(sample, id, mdl):
     index = sample[sample.index == int(id)].index.values
     index = index[0]
     data_client = pd.DataFrame(sample.loc[sample.index, :])
     df_neighbors = pd.DataFrame(knn.fit_predict(data_client), index=data_client.index)
     df_neighbors = pd.concat([df_neighbors, data], axis=1)
     return df_neighbors.iloc[:,1:].sample(10)
                       
 def knn_training(sample):
     knn = KMeans(n_clusters=2).fit(sample)
     return knn

 # Chargement des Données :
    data, sample, target, description = load_data()
    id_client = sample.index.values
    clf = load_model()
