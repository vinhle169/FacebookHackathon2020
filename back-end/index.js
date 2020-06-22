const express = require('express');
const socketio = require('socket.io');
const http = require('http');
const router = require('./router');

const PORT = process.env.PORT || 8008

const app = express();
const server = http.createServer(app);
const io = socketio(server)

const test_message1 = "Hello World!"
const test_message2 = "oh yeah"

io.on('connection', (socket) => {
  console.log("new connection")
  socket.on('join', ({ user_id }) => {
    console.log(`${user_id} connected`)
    // query the previous messages from the database

    socket.emit('response', {message: test_message1})
  });
  socket.on('sendMessage', ({ message }) => {
    // send message to vinh's thing, then get response
    socket.emit('response', {message: test_message2})
  });
  socket.on('disconnect', () => {
    console.log("user left")
  });
});

app.use(router)

server.listen(PORT, () => console.log(`Server started on port ${PORT}`))