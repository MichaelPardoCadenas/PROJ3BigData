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

gameData = 'fields name,url,summary,cover,genres,total_rating,release_dates; where total_rating_count > 100; limit 100;'

responseData = post('https://api.igdb.com/v4/games',
                    headers=headers, data=gameData)
with open('static/json/games.json', 'w') as file:
    json.dump(responseData.json(), file)

def GameItems():
    # Leer JSON games
    with open('static/json/games.json', 'r') as file:
        games = json.load(file)

    # Obtener todas las fechas de lanzamiento
    for game in games:
        # Tomar solo el primer ID de release_dates
        gameID = game['id']
        cover = game['cover']
        genres = game['genres']
        name = game['name']
        summary = game['summary']
        rating = game['total_rating']
        url = game['url']
        releaseDate = game['release_dates'][0]
        
        # Consultar la API para obtener la fecha de lanzamiento en formato humano
        gameDates = f'fields game,human; where id = {releaseDate}; limit 1;'
        responseDates = post('https://api.igdb.com/v4/release_dates',
                            headers=headers, data=gameDates)
        
        # Obtener la fecha de lanzamiento en formato humano
        date = responseDates.json()[0]['human']
        
        # Asignar la fecha de lanzamiento al juego
        game['release_dates'] = date
        # Consultar la API para obtener la cubierta del juego
        gameCover = f'fields url, game, image_id; where id = {cover} ; limit 1;'
        responseCover = post('https://api.igdb.com/v4/covers',
                            headers=headers, data=gameCover)
        # Obtener la url de la cover
        gameCover = responseCover.json()[0]['url']
        gameCoverID = responseCover.json()[0]['image_id']
        gameCover = f"https://images.igdb.com/igdb/image/upload/t_1080p/{gameCoverID}.jpg"
        
        # Asignar la cover
        game['cover'] = gameCover

        # Consultar la API para obtener el genero
        genresList = []
        if len(genres) > 1:
            for i in range(0,2):
                gameGenre = f'fields name; where id = {genres[i]} ; limit 1;'
                responseGenre = post('https://api.igdb.com/v4/genres',
                                    headers=headers, data=gameGenre)
                gameGenre = responseGenre.json()[0]['name']
                genresList.append(gameGenre)
    
        # Asignar el genero
        game['genres'] = genresList

    # Escribir los juegos modificados en el archivo JSON original
    with open('static/json/games.json', 'w') as file:
        json.dump(games, file)

GameItems()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home1.html")

# @app.route("/juego")
# def juego():
#     return render_template("juego.html")


app.run(host='localhost', port=5001, debug=True)