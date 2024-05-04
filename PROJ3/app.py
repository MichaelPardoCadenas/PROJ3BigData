from flask import Flask, render_template
from requests import post
import json
from requests.auth import HTTPBasicAuth

def guardar_en_json(data, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(data, archivo)



# CLIENTID = "w8cmra3o6xppg91h5dbqdl1j6pa0h1"
# CLIENTSECRET = "cbxjyvdot0l7jy0fakznysws0v11xj"
# {
# "access_token": "a70d6z3oa5n5o2mharygi7amnrl285",
# "expires_in": 5177967,
# "token_type": "bearer"
# }

headers = {
    'Client-ID': 'w8cmra3o6xppg91h5dbqdl1j6pa0h1',
    'Authorization': 'Bearer a70d6z3oa5n5o2mharygi7amnrl285',
}

data = 'fields name,url,summary,cover,genres,total_rating,release_dates,age_ratings; where rating_count > 80; limit 500;'

response = post('https://api.igdb.com/v4/games', headers=headers, data=data)
with open('games.json', 'w') as file:
        json.dump(response.json(), file)


# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("home.html")

# app.run(host='localhost', port=5001, debug=True)