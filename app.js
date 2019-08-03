var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors')
var fs=require('fs');
const db = require('./dao')
var app = express();
app.use(cors())

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.post('/order', async (req, res, next) => {
	try{
		var order= req.body;
		var storeId=await db.createNewStore(order);
		var orderId=await db.createNewOrder(order,storeId);
		for(var i=0;i<order.items.length;i++){
			var item=order.items[i];
			var itemId=await db.createNewItem(item);
			var itemtostoreId=await db.assignItemToStore(itemId,storeId,item.item_price);
			await db.addOrderItem(orderId,itemtostoreId,item.item_price,item.item_quantity);
		}
		
		return res.status(200).json({"orderId":orderId})
	}catch(e){
		next(e);
	}
	
});

app.get('/stores',async (req, res, next) => {
	try{
		var stores=await db.getStores();		
		return res.status(200).json({"stores":stores})
	}catch(e){
		next(e);
	}
});
app.get('/stores/:storeId/items',async (req, res, next) => {
	try{
		var query=req.params.storeId;	
		var items=await db.getItemsForStores(query);		
		return res.status(200).json({"items":items})
	}catch(e){
		next(e);
	}
});
app.get('/items/:query',async (req, res, next) => {
	try{
		var query=req.params.query;	
		var items=await db.searchItemsByName(query);		
		return res.status(200).json({"items":items})
	}catch(e){
		next(e);
	}
});
app.get('/stores/:query',async (req, res, next) => {
	try{
		var query=req.params.query;	
		var items=await db.searchStoreByName(query);		
		return res.status(200).json({"stores":items})
	}catch(e){
		next(e);
	}
});
app.get('/item/:itemId/stores',async (req, res, next) => {
	try{
		var query=req.params.itemId;	
		var items=await db.getStoresbyItemId(query);		
		return res.status(200).json({"stores":items})
	}catch(e){
		next(e);
	}
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
