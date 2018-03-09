'use strict';

const process = require('process')


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

const cors = require('cors')
const GCLOUD_STORAGE_BUCKET = "capcollage"

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors())

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

const Storage = require('@google-cloud/storage')

const storage = Storage();
app.set('view engine', 'pug');

const multer = Multer({
	storage: Multer.memoryStorage(),
	limits: {
		fileSize: 5 * 1024 * 1024
	}
})

const bucket = storage.bucket(GCLOUD_STORAGE_BUCKET);

app.get('/', (req, res) => {
  res.render('form.pug');
});

app.post('/upload', multer.single('file'), (req, res, next) => {
  if (!req.file) {
    res.status(400).send('No file uploaded.');
    return;
  }

  // Create a new blob in the bucket and upload the file data.
  const blob = bucket.file(req.file.originalname);
  const blobStream = blob.createWriteStream();

  blobStream.on('error', (err) => {
    next(err);
  });

  blobStream.on('finish', () => {
    // The public URL can be used to directly access the file via HTTP.
    const publicUrl = format(`https://storage.googleapis.com/${bucket.name}/${blob.name}`);
    res.status(200).send(publicUrl);
  });

  blobStream.end(req.file.buffer);
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

/*
app.get('/', (req, res) => {

    res.write('welcome\n');

    runPy.then(function(fromRunpy) {
        console.log(fromRunpy.toString());
        res.end(fromRunpy);
    });
})
*/

//var routes = require('./api/routes/appRoutes');
//routes(app);

