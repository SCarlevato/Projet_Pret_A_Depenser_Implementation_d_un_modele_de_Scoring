# Dependencies
from os import system
from flask import Flask, request, jsonify

import traceback
import pandas as pd
import numpy as np
from prediction_api import *

# Your API definition
app = Flask(__name__)



@app.route('/predictByClientId', methods=['POST'])


if __name__ == '__main__':
    try:
        port = int(system.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345


    app.run(port=port, debug=True)
