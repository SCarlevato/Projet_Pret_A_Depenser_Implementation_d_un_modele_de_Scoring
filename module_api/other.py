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

def load_infos_gen(data):
    
    lst_infos = [data.shape[0],round(data["AMT_INCOME_TOTAL"].mean(), 2),round(data["AMT_CREDIT"].mean(), 2)]
    
    targets = data.TARGET.value_counts()
    
    nb_credits = lst_infos[0]
    
    rev_moy = lst_infos[1]
    
    credits_moy = lst_infos[2]
    
    prop_default = targets
    
    return nb_credits, rev_moy, credits_moy, targets

def load_age_population(data):

    data_age = round((data["DAYS_BIRTH"]/365), 2)
    
    return data_age

def load_income_population():

    df_income = pd.DataFrame(sample["AMT_INCOME_TOTAL"])
    
    df_income = df_income.loc[df_income['AMT_INCOME_TOTAL'] < 200000, :]
    
    return df_income
