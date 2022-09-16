

def load_infos_gen(data):
    
    lst_infos = [data.shape[0],round(data["AMT_INCOME_TOTAL"].mean(), 2),round(data["AMT_CREDIT"].mean(), 2)]
    
    targets = data.TARGET.value_counts()
    
    nb_credits = lst_infos[0]
    
    rev_moy = lst_infos[1]
    
    credits_moy = lst_infos[2]
    
    prop_default = targets
    
    return jsonify({"nb_credits":nb_credits, "rev_moy": rev_moy, "credits_moy": credits_moy})

def load_age_population():

    data_age = round((data["DAYS_BIRTH"]/365), 2)
    
    return json.dumps(list(data_age))

def load_income_population():

    df_income = pd.DataFrame(sample["AMT_INCOME_TOTAL"])
    
    df_income = df_income.loc[df_income['AMT_INCOME_TOTAL'] < 200000, :]
    
    return df_income.to_json(orient='values')
