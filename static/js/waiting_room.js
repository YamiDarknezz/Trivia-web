document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const playerList = document.getElementById("player-list");
    const leaveButton = document.getElementById("leave-room");
    const startButton = document.getElementById("start-game");

    // Recibir actualizaciones en tiempo real de los jugadores en la sala
    socket.on("update_room_players", (data) => {
        if (data.players) {
            playerList.innerHTML = "";
            data.players.forEach((player) => {
                const li = document.createElement("li");
                li.textContent = player;
                playerList.appendChild(li);
            });
        }
    });

    // Salir de la sala
    leaveButton.addEventListener("click", () => {
        const roomName = window.location.pathname.split("/").pop();
        socket.emit("leave_room", { room_name: roomName });
        window.location.href = "/lobby";
    });

    // Comenzar el juego (solo si hay más de un jugador)
    startButton.addEventListener("click", () => {
        const roomName = window.location.pathname.split("/").pop();
        socket.emit("start_game", { room_name: roomName });
    });
});
