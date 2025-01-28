from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Almacenamos las salas en una lista temporal
rooms = []
players = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if request.method == 'POST':
        # Al ingresar el nombre, el jugador se registrará
        username = request.form['username']
        # Crear una sala nueva si no existe
        room_name = request.form['room_name']
        
        if room_name not in rooms:
            rooms.append(room_name)
        
        # Registramos al jugador en la sala
        players[username] = room_name
        return redirect(url_for('game', room_name=room_name))
    
    return render_template('lobby.html', rooms=rooms)

@app.route('/game/<room_name>')
def game(room_name):
    # Aquí se mostrará la lista de jugadores en la sala
    room_players = [player for player, room in players.items() if room == room_name]
    return render_template('game.html', room_name=room_name, players=room_players)

if __name__ == '__main__':
    app.run(debug=True)
