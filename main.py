from flask import Flask, request, render_template, redirect, url_for
import requests
from urllib.parse import quote

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

SCRIPT_URL = os.getenv('SCRIPT_URL')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():
    name = request.form.get('nameInput')
    if not name:
        return render_template('index.html', msg="Please enter a name.")

    data_dict = get_data(name)
    if data_dict:
        name = data_dict.get('name')
        sessions = ", ".join(map(str, data_dict.get('sessions', [])))
        totalHours = data_dict.get('totalHours')
        if totalHours > 0:
            return render_template('index.html', name=name, sessions=sessions, totalHours=totalHours)
        else:
            return render_template('index.html', name=name, msg="You did not attend any sessions.")
    else:
        return render_template('index.html', msg="Failed to retrieve data. Please try again.")

def get_data(name) -> dict:
    encoded_name = quote(name)
    try:
        print("Fetching data from Google Apps Script...")
        response = requests.get(f"{SCRIPT_URL}?name={encoded_name}")
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return None
    except ValueError as ve:
        print("❌ Error decoding JSON:", ve)
        return None

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
