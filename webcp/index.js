const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

// endpoints
app.get('/:endpointName', (req, res) => {
    const endpointName = req.params.endpointName;
    res.sendFile('/home/requin/controller/' + endpointName);
});

app.get('/', (req, res) => {
    const endpointName = req.params.endpointName;
    res.sendFile('/home/requin/controller/index.html');
});

// server
server.listen(3000, () => {
    console.log('listening on *:3000');
});
