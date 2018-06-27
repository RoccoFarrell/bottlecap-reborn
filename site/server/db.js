//MySQL config

var mysql = require('mysql');
var db;

function connectDatabase () {
	if(!db) {
		db = mysql.createConnection({
		  host: "localhost",
		  user: "root",
		  password: "Paytr0n1x",
		  database: 'apps'
		});

		db.connect(function(err) {
		  if (err) throw err;
		  console.log("Connected to MYSQL DB!");
		});
	}
	return db;
}

module.exports = connectDatabase();