// import firebase from 'firebase'
var firebase = require('firebase')
var express = require('express')
var bodyParser = require('body-parser')

// Initialize Firebase
// TODO: Replace with your project's customized code snippet
var config = {
    apiKey: "<API_KEY>",
    authDomain: "<PROJECT_ID>.firebaseapp.com",
    databaseURL: "https://<DATABASE_NAME>.firebaseio.com",
    storageBucket: "<BUCKET>.appspot.com",
  };

const firebaseApp = firebase.initializeApp(config);
const app = express()

let runPy = new Promise(function(success, nosuccess) {

    const pyfile = "../image.py"
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
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors())


const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

app.get('/', (req, res) => {

    res.write('welcome\n');

    runPy.then(fromRunpy => {
        console.log(fromRunpy.toString());
        res.end(fromRunpy);
    })
    .catch(error => {
        console.log("error")
        console.log(error.toString())
    });
})
