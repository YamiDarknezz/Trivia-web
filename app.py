from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Diccionario para almacenar las salas y los jugadores en ellas
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if request.method == 'POST':
        # Crear una nueva sala
        room_name = request.form.get('room_name')
        if room_name and room_name not in rooms:
            rooms[room_name] = []  # Lista vacía de jugadores
        return redirect(url_for('lobby'))
    
    return render_template('lobby.html', rooms=rooms)

@app.route('/game/<room_name>')
def game(room_name):
    if room_name in rooms:
        return render_template('game.html', room_name=room_name)
    else:
        return "Sala no encontrada.", 404

if __name__ == '__main__':
    app.run(debug=True)
