const Pool = require('pg').Pool
const pool = new Pool({
  user: 'postgres',
  host: '134.209.155.59',
//  host: '192.168.0.12', local testing ip should be mentioned
  database: 'postgres',
  password: 'psql123',
  port: 5432
})
var category={
	"food":1,
	"grocery":2,
	"others":3
}
async function getStoreByNameAndAddress(name,address){
	try{
		 const q1 = {
				   text: 'SELECT store_id FROM stores where store_name=$1 and store_address=$2',
				   values: [name,address]
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows[0].store_id;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function addNewStore(data){
	try{
	 const q1 = {
		      text: 'insert into stores (store_name,store_address,pincode,info) values ($1,$2,$3,$4) returning store_id',
		      values: [data.store_name,data.store_address,data.store_pincode,JSON.stringify(data.store_info)]
		    }
	 var rows= await queryExecutor(q1);
	  if(rows) return rows[0].store_id;	
	}catch(e){
		console.log(error)
	}
	
	  return null;
}
async function createNewStore(data){
	try{
		var storeId=await getStoreByNameAndAddress(data.store_name,data.store_address);
		if(storeId!=null)
			return storeId;
		else
			return await addNewStore(data);	
	}catch(e){
		console.log(error)
	}
	return null;
}
async function createNewOrder(data,storeId){
	try{
		 const q1 = {
			      text: 'insert into orders (store_frn_id,info,order_total,order_date) values ($1,$2,$3,$4) returning order_id',
			      values: [storeId,JSON.stringify(data.order_info),data.order_total,new Date()]
			    }
		 var rows= await queryExecutor(q1);
		  if(rows) return rows[0].order_id;	
		}catch(e){
			console.log(error)
		}
		
		  return null;
}
async function getItemByName(name){
	try{
		 const q1 = {
				   text: 'SELECT item_id FROM items where item_name=$1',
				   values: [name]
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows[0].item_id;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function addNewItem(name,price,category_id){
	try{
	 const q1 = {
		      text: 'insert into items (item_name,lowest_price,category_frn_id) values ($1,$2,$3) returning item_id',
		      values: [name,price,category_id]
		    }
	 var rows= await queryExecutor(q1);
	  if(rows) return rows[0].item_id;	
	}catch(e){
		console.log(error)
	}
	
	  return null;
}
async function createNewItem(data){
	try{
		var itemId=await getItemByName(data.item_name);
		if(itemId!=null)
			return itemId;
		else{
			var catId=category[data.item_category];
			return await addNewItem(data.item_name,data.item_price,catId);	
		}
			
	}catch(e){
		console.log(error)
	}
	return null;
}

async function getItemToStore(itemId,storeId){
	try{
		 const q1 = {
				   text: 'SELECT item_store_id FROM item_to_store where item_frn_id=$1 and store_frn_id=$2',
				   values: [itemId,storeId]
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows[0].item_store_id;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function addItemToStore(itemId,storeId,price){
	try{
	 const q1 = {
		      text: 'insert into item_to_store (item_frn_id,store_frn_id,item_latest_price) values ($1,$2,$3) returning item_store_id',
		      values: [itemId,storeId,price]
		    }
	 var rows= await queryExecutor(q1);
	  if(rows) return rows[0].item_store_id;	
	}catch(e){
		console.log(error)
	}
	
	  return null;
}
async function assignItemToStore(itemId,storeId,item_price){
	try{
		var exitemId=await getItemToStore(itemId,storeId);
		if(exitemId!=null)
			return exitemId;
		else{
			return await addItemToStore(itemId,storeId,item_price);	
		}
			
	}catch(e){
		console.log(error)
	}
	return null;
}
async function addOrderItem(orderId,itemtostoreId,item_price,item_quantity){
	try{
	 const q1 = {
		      text: 'insert into order_items (order_frn_id,item_store_frn_id,price,quantity) values ($1,$2,$3,$4) returning order_frn_id',
		      values: [orderId,itemtostoreId,item_price,item_quantity]
		    }
	 var rows= await queryExecutor(q1);
	  if(rows) return rows[0].order_frn_id;	
	}catch(e){
		console.log(error)
	}
	
	  return null;
}
async function getStores(){
	try{
		 const q1 = {
				   text: 'SELECT * FROM stores limit 100'
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function getCatagories(){
	try{
		 const q1 = {
				   text: 'SELECT * FROM category'
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function getItemsByCategoryId(query){
	try{
		 const q1 = {
				   text: 'SELECT * FROM items where category_frn_id=$1 limit 100',
				   values:[query]
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function searchItemsByName(query){
	try{
		 const q1 = {
				   text: 'SELECT * FROM items where item_name ILIKE $1 limit 100',
				   values:['%' + query + '%']
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function searchStoreByName(query){
	try{
		 const q1 = {
				   text: 'SELECT * FROM stores where store_name ILIKE $1 limit 100',
				   values:['%' + query + '%']
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function getItemsForStores(storeId){
	try{
		 const q1 = {
				   text: 'select  i.item_id,i.item_name,s.item_latest_price as item_price from item_to_store as s inner join items as i on i.item_id=s.item_frn_id  where s.store_frn_id=$1 limit 100',
				   values: [storeId]
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function getStoresbyItemId(itemId){
	try{
		 const q1 = {
				   text: 'select  i.*,s.item_latest_price as item_price from item_to_store as s inner join stores as i on i.store_id=s.store_frn_id  where s.item_frn_id=$1 order by s.item_latest_price limit 100',
				   values: [itemId]
				 }
	  var rows= await queryExecutor(q1);
	  if(rows) return rows;
	}catch(e){
		console.log(error)
	} 
	  return null;
}
async function queryExecutor(queryObj){
	try{
		let response = await pool.query(queryObj);
		 if(response && response.rows.length){
			 return response.rows
		 } else{
			 return null;
		 }
				 
	}catch(e){
		console.log(e)
		return null;
	}
    
}
module.exports= {
		createNewStore,createNewOrder,createNewItem,assignItemToStore,addOrderItem,searchItemsByName,getItemsForStores,getStores,searchStoreByName,getStoresbyItemId,getCatagories,getItemsByCategoryId
}