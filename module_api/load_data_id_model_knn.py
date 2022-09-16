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
import streamlit as st
import streamlit.components.v1 as components

plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')

def load_data():
    
    z = ZipFile("data/data_final.zip")
    
    data = pd.read_csv(z.open('data_final.csv'), index_col='SK_ID_CURR', encoding ='utf-8')
                       
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
                       
def identite_client(data, id):
                       
     data_client = data[data.index == int(id)]
                       
     return data_client                    
                                    
def load_prediction(sample, id, clf):
        
    X=sample.iloc[:, :-1]
                       
    score = clf.predict_proba(X[X.index == int(id)])[:,1]
                       
    return score                                             
