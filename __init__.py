from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from collections import Counter
import requests
from datetime import datetime
from flask import render_template

app = Flask(__name__)  


@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    
    try:
        data = response.json()
    except Exception as e:
        return f"Erreur lors de la lecture de l'API GitHub : {e}"

    # Vérifie si c’est une erreur de quota GitHub
    if isinstance(data, dict) and data.get('message'):
        return f"Erreur GitHub : {data['message']}"

    minutes_list = []

    for commit in data:
        try:
            date_str = commit["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_obj.strftime('%H:%M'))
        except Exception as e:
            print(f"Erreur dans un commit : {e}")
            continue

    if not minutes_list:
        return "Aucun commit trouvé ou problème dans les données."

    minute_counts = Counter(minutes_list)
    minutes = list(minute_counts.keys())
    counts = list(minute_counts.values())

    return render_template("commits.html", minutes=minutes, counts=counts)
        
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhisto():
    return render_template("histogramme.html")

@app.route("/contact/")
def affichecontact():
    return render_template("contact.html")

  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route('/')
def hello_world():
    return render_template('hello.html')
  
if __name__ == "__main__":
  app.run(debug=True)
