var express = require('express');
var bodyParser = require('body-parser');
var expressHbs = require('express3-handlebars');
var socket = require('./socket.js').socket;
var socket_send = require('./socket.js').send;


var sockets = express();
var sockets_server = require('http').createServer(sockets);
socket.installHandlers(sockets_server, {prefix: '/socket'});
sockets_server.listen(1338, '0.0.0.0');

var app = express();
var router = express.Router();

app.use(bodyParser());

app.set('views', __dirname + '/views');
app.engine('hbs', expressHbs({extname:'hbs'}));
app.set('view engine', 'hbs');

var message = "No messages yet";

router.use(function(req, res, next) {
  console.log('%s %s %s', req.method, req.url, req.path);
  next();
});

router.use(express.static(__dirname + '/static'));

router.get('/', function(req, res) {
  res.render('home', {message: message});
});

router.post('/message', function(req, res) {
  message = req.body.message;
  res.send('Updated!');
  socket_send(message);
});


app.use('/', router);

app.listen(1337);
console.log("It's at port 1337!");
