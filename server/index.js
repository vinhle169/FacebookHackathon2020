const express = require('express');
const socketio = require('socket.io');
const http = require('http');
const router = require('./router');

const PORT = process.env.PORT || 8008

const app = express();
const server = http.createServer(app);
const socket = socketio(server)

app.use(router)

server.listen(PORT, () => console.log(`Server started on port ${PORT}`))