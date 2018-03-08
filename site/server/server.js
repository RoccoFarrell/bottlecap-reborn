'use strict';

var mysql = require('mysql');
const express = require('express'),
	app = express(),
	port = process.env.PORT || 8081,
	mongoose = require('mongoose'),
	bodyParser = require('body-parser'),
	Multer = require('multer'),
	format = require('util').format
	//db = require('./db');

let runPy = new Promise(function(success, nosuccess) {

    const pyfile = "../../image.py"
    const { spawn } = require('child_process');
    const pyprog = spawn('python',[ pyfile ]);

    pyprog.stdout.on('data', function(data) {
        success(data);
    });
    pyprog.stderr.on('data', (data) => {
        nosuccess(data);
    });
});

app.get('/', (req, res) => {

    res.write('welcome\n');

    runPy.then(function(fromRunpy) {
        console.log(fromRunpy.toString());
        res.end(fromRunpy);
    });
})

const cors = require('cors')

//Mongoose config
/*
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/apps',{
	useMongoClient: true
}, function(error){
	if(error) throw error;
	console.log("Connected to Mongo DB!")
});
*/

//-------------------------------

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors())

//var routes = require('./api/routes/appRoutes');
//routes(app);

app.listen(port);

console.log('RESTful API online at ' + port);