var sock = require('sockjs');

var echo = sock.createServer();

connections = {};

echo.on('connection', function (conn) {
  connections[conn.id] = conn;
  console.log('connection!');

  conn.on('close', function () {
    delete connections[conn.id];
    console.log('lost connection');
  });
});

function send(message) {
  for (conn_id in connections) {
    connections[conn_id].write(message);
  }
};

module.exports = {socket: echo, send: send};
