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
    console.log(`${user_id} connected`)
    // query the previous messages from the database
    socket.emit('loadPast', {messages: 'FIXME: SEND THE PAST MESSAGES'})
  });
  socket.on('sendMessage', ({ message }) => {
    // send message to vinh's thing, then get response
    socket.emit('response', {response: 'FIXME: send the response message'})
  });
  socket.on('disconnect', () => {
    console.log("user left")
  });
});

app.use(router)

server.listen(PORT, () => console.log(`Server started on port ${PORT}`))