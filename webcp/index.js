const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const Server = require("socket.io");
const io = new Server(server);
const net = require('net');



app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', (websock) => {
    console.log('a user connection');
    var rawsock = net.connect({port:50079}, function() {
	console.log('cp_sock connected to cp_server');
    });
    rawsock.on('error', function(data) {
	console.log("cp_sock closed by error");
    });

    var buffer = "";
    rawsock.on('data', function(data) {
	console.log("cp_sock got " + data.toString());
	buffer += data;
	const parts = buffer.split('\n');
	if (parts.length > 1) {
	    buffer = parts[parts.length - 1];
	    const messages = parts.slice(0, parts.length - 1);
	    for (let m of messages) {
		websock.emit('msg', m.toString());
	    }
	}
    });
    
    websock.on('disconnect', () => {
	rawsock.destroy();
	console.log('user disconnected');
    });
    websock.on('msg', (msg) => {
	//console.log('msg', msg);
	console.log("from browser :" + msg);
	rawsock.write(msg + '\n');
    });
});


server.listen(3000, () => {
    console.log('listening on *:3000');
});
