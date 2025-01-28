from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret-key-for-session'

# Simular datos en memoria
players = []  # Lista de jugadores activos en el lobby
rooms = {}    # Diccionario con salas y jugadores dentro de cada sala


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if username:
        session['username'] = username  # Guardar nombre en la sesión
        if username not in players:
            players.append(username)  # Agregar a la lista de jugadores activos
        return redirect(url_for('lobby'))
    return redirect(url_for('index'))


@app.route('/lobby')
def lobby():
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('lobby.html', username=username, players=players, rooms=rooms)


@app.route('/create_room', methods=['POST'])
def create_room():
    room_name = request.form.get('room_name')
    username = session.get('username')
    if room_name and username:
        if room_name not in rooms:
            rooms[room_name] = [username]  # Crear sala y agregar al creador
        return redirect(url_for('room', room_name=room_name))
    return redirect(url_for('lobby'))


@app.route('/room/<room_name>')
def room(room_name):
    username = session.get('username')
    if not username or room_name not in rooms:
        return redirect(url_for('lobby'))
    if username not in rooms[room_name]:
        rooms[room_name].append(username)  # Agregar jugador a la sala
    return render_template('game.html', username=username, room_name=room_name, players=rooms[room_name])


@app.route('/leave_room/<room_name>')
def leave_room(room_name):
    username = session.get('username')
    if username and room_name in rooms and username in rooms[room_name]:
        rooms[room_name].remove(username)
        if not rooms[room_name]:  # Eliminar sala si está vacía
            del rooms[room_name]
    return redirect(url_for('lobby'))


@app.route('/logout')
def logout():
    username = session.pop('username', None)
    if username in players:
        players.remove(username)
    for room in rooms.values():
        if username in room:
            room.remove(username)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
