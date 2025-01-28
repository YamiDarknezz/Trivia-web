// Conexión al WebSocket del servidor
const socket = io.connect('http://' + document.domain + ':' + location.port);

// Manejador para abrir la conexión
socket.onopen = function () {
    console.log('Conectado al WebSocket del lobby.');
};

// Manejador para recibir mensajes
socket.on('update_players', function(data) {
    const playerList = document.querySelector('#player-list ul');
    playerList.innerHTML = '';
    data.players.forEach(player => {
        const li = document.createElement('li');
        li.textContent = player;
        playerList.appendChild(li);
    });
});

socket.on('update_rooms', function(data) {
    const roomManagement = document.querySelector('#room-management');
    const roomList = roomManagement.querySelector('ul');
    roomList.innerHTML = '';
    if (data.rooms.length > 0) {
        data.rooms.forEach(room => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${room.name} - Jugadores: ${room.players.length}
                <form action="/join_room" method="POST" style="display: inline;">
                    <input type="hidden" name="room_name" value="${room.name}">
                    <button type="submit">Unirse</button>
                </form>
            `;
            roomList.appendChild(li);
        });
    } else {
        roomManagement.innerHTML = '<p>No hay salas disponibles.</p>';
    }
});

// Manejador para cerrar la conexión
socket.onclose = function () {
    console.log('Conexión cerrada con el WebSocket del lobby.');
};

// Manejador para errores
socket.onerror = function (error) {
    console.error('Error en el WebSocket:', error);
};
