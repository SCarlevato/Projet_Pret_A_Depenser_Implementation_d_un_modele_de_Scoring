# Importations :
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
from MODULES_API.load_data_id_model_knn import *
from MODULES_API.informations_client import *
plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')

def main() :
 
    # Chargement des Données :
    data, sample, target, description = load_data()
    id_client = sample.index.values
    clf = load_model()
    
    #######################################
    # SIDEBAR #
    #######################################

    # Présentation du Titre :
    html_temp = """
    <div style="background-color: tomato; padding:10px; border-radius:10px">
    <h1 style="color: white; text-align:center">Dashboard Scoring Credit</h1>
    </div>
    <p style="font-size: 20px; font-weight: bold; text-align:center">Support de Décision de Crédit</p>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Sélection ID Client :
    st.sidebar.header("**Informations Générales**")

    # Chargement Case à Cocher :
    chk_id = st.sidebar.selectbox("Client ID", id_client)

    # Chargement Informations Générales :
    nb_credits, rev_moy, credits_moy, targets = load_infos_gen(data)

    ### Présentation des Informations dans la Sidebar ###
    # Nombre d'Emprunts dans l'Echantillon :
    st.sidebar.markdown("<u>Nombre d'Emprunts dans notre Panel :</u>", unsafe_allow_html=True)
    st.sidebar.text(nb_credits)

    # Revenu Moyen :
    st.sidebar.markdown("<u>Revenu Moyen (USD) :</u>", unsafe_allow_html=True)
    st.sidebar.text(rev_moy)

    # AMT CREDIT :
    st.sidebar.markdown("<u>Amortissement Crédit (USD) :</u>", unsafe_allow_html=True)
    st.sidebar.text(credits_moy)
    
    # PieChart :
    st.sidebar.markdown("<u>......</u>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5,5))
    plt.pie(targets, explode=[0, 0.1], labels=['No default', 'Default'], autopct='%1.1f%%', startangle=90)
    st.sidebar.pyplot(fig)
        
    #######################################
    # PAGE D'ACCUEIL #
    #######################################
    
    # Présentation ID Client Sidebar :
    st.write("Sélection ID Client :", chk_id)

    # Présentation Information Client : Genre, Age, Statut Familial, Enfants :
    st.header("**Présentation Information Client**")

    if st.checkbox("Présentation Information Client :"):

        infos_client = identite_client(data, chk_id)
        st.write("**Genre : **", infos_client["CODE_GENDER"].values[0])
        st.write("**Age : **{:.0f} ans".format(int(infos_client["DAYS_BIRTH"]/365)))
        st.write("**Statut Familial : **", infos_client["NAME_FAMILY_STATUS"].values[0])
        st.write("**Nombre d'Enfants : **{:.0f}".format(infos_client["CNT_CHILDREN"].values[0]))

        # Graphique de Distribution des Ages :
        data_age = load_age_population(data)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(data_age, edgecolor = 'k', color="goldenrod", bins=20)
        ax.axvline(int(infos_client["DAYS_BIRTH"].values / 365), color="green", linestyle='--')
        ax.set(title='Age Client', xlabel='Age(Année)', ylabel='')
        st.pyplot(fig)
    
        st.subheader("*Revenu (USD)*")
        st.write("**Revenu total : **{:.0f}".format(infos_client["AMT_INCOME_TOTAL"].values[0]))
        st.write("**Quantité de Crédit : **{:.0f}".format(infos_client["AMT_CREDIT"].values[0]))
        st.write("**Annuités : **{:.0f}".format(infos_client["AMT_ANNUITY"].values[0]))
        st.write("**Valeurs des Biens pour l'Octroi de Crédit : **{:.0f}".format(infos_client["AMT_GOODS_PRICE"].values[0]))
        
        # Graphique de Distribution de Revenus :
        data_income = load_income_population(data)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(data_income["AMT_INCOME_TOTAL"], edgecolor = 'k', color="goldenrod", bins=10)
        ax.axvline(int(infos_client["AMT_INCOME_TOTAL"].values[0]), color="green", linestyle='--')
        ax.set(title='Revenu Client', xlabel='Revenu (USD)', ylabel='')
        st.pyplot(fig)
        
        # Age / Graphique de Distribution de Revenu Total :
        data_sk = data.reset_index(drop=False)
        data_sk.DAYS_BIRTH = (data_sk['DAYS_BIRTH']/365).round(1)
        fig, ax = plt.subplots(figsize=(10, 10))
        fig = px.scatter(data_sk, x='DAYS_BIRTH', y="AMT_INCOME_TOTAL",
                         size="AMT_INCOME_TOTAL", color='CODE_GENDER',
                         hover_data=['NAME_FAMILY_STATUS', 'CNT_CHILDREN', 'NAME_CONTRACT_TYPE', 'SK_ID_CURR'])

        fig.update_layout({'plot_bgcolor':'#f0f0f0'},
                          title={'text':"Age / Revenu Total", 'x':0.5, 'xanchor': 'center'},
                          title_font=dict(size=20, family='Verdana'), legend=dict(y=1.1, orientation='h'))

        fig.update_traces(marker=dict(line=dict(width=0.5, color='#3a352a')), selector=dict(mode='markers'))
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#f0f0f0', gridcolor='#cbcbcb',
                         title="Age", title_font=dict(size=18, family='Verdana'))
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#f0f0f0', gridcolor='#cbcbcb',
                         title="Income Total", title_font=dict(size=18, family='Verdana'))

        st.plotly_chart(fig)
    
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)

    # Présentation Solvabilité du Client :
    st.header("**Analyse Fichier Client**")
    prediction = load_prediction(sample, chk_id, clf)
    st.write("**Probabilité Défaut : **{:.0f} %".format(round(float(prediction)*100, 2)))

    if prediction <= 0.70 :
       decision = "<font color='green'>**EMPRUNT ACCEPTE**</font>"
    else:
       decision = "<font color='red'>**EMPRUNT REJETE**</font>"

    st.write("**Decision** *(avec seuil 70%)* **: **", decision, unsafe_allow_html=True)

    st.markdown("<u>Données Client :</u>", unsafe_allow_html=True)
    st.write(identite_client(data, chk_id))

    # Feature Importance / Description :
    if st.checkbox("ID Client {:.0f} Feature Importance :".format(chk_id)):
        shap.initjs()
        X = sample.iloc[:, :-1]
        X = X[X.index == chk_id]
        number = st.slider("Sélectionner un Nombre de Features :", 0, 20, 5)

        fig, ax = plt.subplots(figsize=(10, 10))
        explainer = shap.TreeExplainer(load_model())
        shap_values = explainer.shap_values(X)
        shap.summary_plot(shap_values[0], X, plot_type ="bar", max_display=number, color_bar=False, plot_size=(5, 5))
        st.pyplot(fig)
        
        if st.checkbox("Aide :") :
            list_features = description.index.to_list()
            feature = st.selectbox('Feature Checklist', list_features)
            st.table(description.loc[description.index == feature][:1])
        
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)
            
    # Présentation des Dossiers de Clients Similaires :
    @st.cache(allow_output_mutation=True)
    def load_knn(sample):
        knn = knn_training(sample)
        return knn
    
    @st.cache
    def load_kmeans(sample, id, mdl):
        index = sample[sample.index == int(id)].index.values
        index = index[0]
        data_client = pd.DataFrame(sample.loc[sample.index, :])
        df_neighbors = pd.DataFrame(knn.fit_predict(data_client), index=data_client.index)
        df_neighbors = pd.concat([df_neighbors, data], axis=1)
        return df_neighbors.iloc[:,1:].sample(10)
                       
    @st.cache
    def knn_training(sample):                 
        knn = KMeans(n_clusters=2).fit(sample)              
        return knn
    
    chk_voisins = st.checkbox("Observations des Autres Dossiers Clients :")

    if chk_voisins:
        knn = load_knn(sample)
        st.markdown("<u>Liste des 10 Clients les Plus Proches :</u>", unsafe_allow_html=True)
        st.dataframe(load_kmeans(sample, chk_id, knn))
        st.markdown("<i>Target 1 = Client avec Défaut</i>", unsafe_allow_html=True)
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)
        
    st.markdown('***')
    st.markdown("Merci de votre attention.")
    
if __name__ == '__main__':
    main()
