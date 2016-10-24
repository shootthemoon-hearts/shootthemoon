/**
 * This is the script that is used to create the server. Create the server by
 * calling:
 * 
 * node index.js
 * 
 */

// Import the Express module
var express = require('express');

// Import the 'path' module (packaged with Node.js)
var path = require('path');

// Create a new instance of Express
var app = express();

// Serve static html, js, css, and image files from the 'client' directory
app.use(express.static(path.join(__dirname,'client')));

// Create a Node.js based http server on port 8080
var server = require('http').createServer(app).listen(process.env.PORT || 8080);

// Create a Socket.IO server and attach it to the http server
var io = require('socket.io').listen(server);


// Start the game manager
var gamemanager = require('./gamemanager');
gamemanager.start(io);