var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors')
var fs=require('fs');
const Pool = require('pg').Pool
const pool = new Pool({
  user: 'postgres',
  host: '134.209.155.59',
  database: 'postgres',
  password: 'psql123',
  port: 5432
})
var app = express();
app.use(cors())

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.get("/test",function(req,res,next){
	return res.status(200).json({"message":"success"})
});

//centralized error handler
app.use((err, req, res, next) => {
  // log the error...
  console.error(err)
  if(err.httpStatusCode == null || err.httpStatusCode == undefined)
    err.httpStatusCode = 500;
  res.sendStatus(err.httpStatusCode).json(err)
})

module.exports = app;
