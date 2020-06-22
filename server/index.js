const express = require('express');
const socketio = require('socket.io');
const http = require('http');
const router = require('./router');

const PORT = process.env.PORT || 8008

const app = express();
const server = http.createServer(app);
const io = socketio(server)

io.on('connection', (socket) => {
  console.log("new connection")
  socket.on('join', ({ user_id }) => {
    console.log(`${user_id} joined`)
    socket.emit('FIXME: SEND THE MESSAGES')
  });
  socket.on('sendMessage', ({ message }) => {
    socket.emit('FIXME: send the message')
  });
  socket.on('disconnect', () => {
    console.log("user left")
  });
});

app.use(router)

server.listen(PORT, () => console.log(`Server started on port ${PORT}`))