const express = require('express');
const path = require('path');

const app = express();


app.use(express.static('/home/requin/controller'));

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
app.listen(3000, () => {
    console.log('listening on *:3000');
});
