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
                       
def load_prediction(sample, id, clf):
        
    X=sample.iloc[:, :-1]
                       
    score = clf.predict_proba(X[X.index == int(id)])[:,1]
                       
    return score
                                          
def identite_client(data, id):
                       
     data_client = data[data.index == int(id)]
                       
     return data_client
                       
 def load_knn(sample):
                       
     knn = knn_training(sample)
                       
    return knn                      
                       
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
