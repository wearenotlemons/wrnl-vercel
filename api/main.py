from flask import Flask, request, render_template, jsonify
import requests
from urllib.parse import quote
import os

app = Flask(__name__, template_folder="..")  # Assuming index.html is in root

SCRIPT_URL = os.environ.get("SCRIPT_URL")

@app.route("/", methods=["GET", "POST"])
def handle():

    # Get comments from comments.txt
    with open("comments.txt", "r") as f:
        comments = f.readline() # Only takes first line of comments.txt

    if request.method == "GET":
        return render_template("index.html")

    name = request.form.get("nameInput")
    if not name:
        return render_template("index.html", msg="Please enter a name.")

    data = get_data(name)
    if data:
        name = data.get("name")
        sessions = ", ".join(map(str, data.get("sessions", [])))
        totalHours = data.get("totalHours")
        remarks = data.get("remarks")
        if totalHours > 0:
            return render_template("index.html", name=name, comments=comments, sessions=sessions, totalHours=totalHours, remarks=remarks)
        else:
            return render_template("index.html", name=name, msg="You did not attend any sessions.", remarks=remarks)
    else:
        return render_template("index.html", msg="Failed to retrieve data. Please try again.")

def get_data(name):
    encoded_name = quote(name)
    try:
        print("Fetching data from Google Apps Script...")
        response = requests.get(f"{SCRIPT_URL}?name={encoded_name}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error fetching data:", e)
        return None
