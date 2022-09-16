# Dependencies
from os import system
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import numpy as np

# Your API definition
app = Flask(__name__)

@app.route('/infos_gen', methods=['POST'])

def load_infos_gen(data):
    
    lst_infos = [data.shape[0],round(data["AMT_INCOME_TOTAL"].mean(), 2),round(data["AMT_CREDIT"].mean(), 2)]
    
    targets = data.TARGET.value_counts()
    
    nb_credits = lst_infos[0]
    
    rev_moy = lst_infos[1]
    
    credits_moy = lst_infos[2]
    
    prop_default = targets
    
    return jsonify({"nb_credits":nb_credits, "rev_moy": rev_moy, "credits_moy": credits_moy})

if __name__ == '__main__':
    try:
        port = int(system.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345

    app.run(port=port, debug=True)