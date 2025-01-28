from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# Variables globales para jugadores y salas
players = []
rooms = {}

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Manejar el registro del nombre del jugador
@app.route('/game', methods=['POST'])
def game():
    username = request.form.get('username')
    if username and username not in players:
        players.append(username)
        # Emitir actualización a todos los clientes conectados
        socketio.emit('update_players', {'players': players})
    elif username in players:
        # Podrías manejar este caso con un mensaje de error
        pass
    return redirect(url_for('lobby'))

# Página del lobby
@app.route('/lobby')
def lobby():
    return render_template('lobby.html', players=players, rooms=rooms)

# Crear una sala
@app.route('/create_room', methods=['POST'])
def create_room():
    room_name = request.form.get('room_name')
    if room_name and room_name not in rooms:
        rooms[room_name] = {'name': room_name, 'players': [], 'host': request.form.get('username')}
        # Emitir actualización de salas a todos los clientes conectados
        socketio.emit('update_rooms', {'rooms': list(rooms.values())})
    return redirect(url_for('lobby'))

@socketio.on('join_room')
def handle_join_room(data):
    room_name = data['room_name']
    username = data['username']
    if room_name in rooms:
        rooms[room_name]['players'].append(username)
        join_room(room_name)  # Unir al jugador a la sala
        # Emitir los jugadores de la sala a los demás en esa sala
        emit('update_room_players', {'players': rooms[room_name]['players']}, room=room_name)
        # Emitir actualización de salas
        emit('update_rooms', {'rooms': list(rooms.values())})

@app.route('/join_room', methods=['POST'])
def join_room_route():
    room_name = request.form.get('room_name')
    username = request.form.get('username')
    if room_name and username:
        # Emitir evento 'join_room' para manejar la unión de la sala en el lado del cliente
        socketio.emit('join_room', {'room_name': room_name, 'username': username})
    return redirect(url_for('lobby'))

# Página de la sala de espera
@app.route('/waiting_room/<room_name>')
def waiting_room(room_name):
    if room_name not in rooms:
        return redirect(url_for('lobby'))
    return render_template('waiting_room.html', room=rooms[room_name], players=players)

# WebSocket para el lobby
@socketio.on('connect')
def handle_connect():
    # Emitir la lista de jugadores y salas a todos los conectados
    emit('update_players', {'players': players})
    emit('update_rooms', {'rooms': list(rooms.values())})

@socketio.on('disconnect')
def handle_disconnect():
    disconnected_player = None
    for player in players:
        # Aquí puedes añadir lógica para identificar el jugador desconectado si es necesario
        disconnected_player = player
        break
    
    if disconnected_player:
        players.remove(disconnected_player)
        for room in rooms.values():
            if disconnected_player in room['players']:
                room['players'].remove(disconnected_player)
                # Emitir la actualización de la lista de jugadores a esa sala
                emit('update_room_players', {'players': room['players']}, room=room['name'])
        
        # Emitir la actualización global de jugadores
        emit('update_players', {'players': players})

# Iniciar el servidor
if __name__ == '__main__':
    socketio.run(app, debug=True)
