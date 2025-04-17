from flask import Flask, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from collections import Counter

app = Flask(__name__)  

# ✅ ROUTE COMMITS avec urllib (PAS de requests)
@app.route('/commits/')
def affichecommits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    try:
        response = urlopen(url)
        raw_data = response.read()
        data = json.loads(raw_data.decode("utf-8"))
    except Exception as e:
        return f"Erreur lors de l'appel à l'API GitHub : {e}"

    minutes_list = []
    for commit in data:
        try:
            date_str = commit.get("commit", {}).get("author", {}).get("date")
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minutes_list.append(date_obj.strftime('%H:%M'))
        except Exception as e:
            print(f"Erreur: {e}")

    if not minutes_list:
        return "Aucun commit valide trouvé."

    minute_counts = Counter(minutes_list)
    minutes = list(minute_counts.keys())
    counts = list(minute_counts.values())

    return render_template("commits.html", minutes=minutes, counts=counts)


# ✅ AUTRES ROUTES
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhisto():
    return render_template("histogramme.html")

@app.route("/contact/")
def affichecontact():
    return render_template("contact.html")

@app.route("/tawarano/")
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# ✅ Lancement
if __name__ == "__main__":
    app.run(debug=True)
