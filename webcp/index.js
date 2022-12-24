const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

var x = 0;

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
    /*console.log(x);
    if (x == 0) {
	res.sendFile(__dirname + '/test.html');
	x = 1;
    } else {
	res.sendFile(__dirname + '/index.html');
	x = 0;
    }
    console.log(x);
    console.log("-");*/
});


server.listen(3000, () => {
    console.log('listening on *:3000');
});
