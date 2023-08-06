import json
import requests

class api:
  def __init__(self,apikey,apisecret,broker,version="1.0"):
     self.apikey=apikey 
     self.apisecret=apisecret
     self.burl = "https://" + broker + 'api.algomojo.com/' + str(version) + '/'
  def place_order(self,ticker,exchange,action,ordertype,qty,product,prc=0,dscqty=0,trgprc="0"):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                       "stgy_name":"Test Strategy",
                       "symbol":ticker,
                       "exchange":exchange,
                       "transaction_type":action,
                       "duration":"DAY",
                       "order_type":ordertype,
                       "quantity":qty,
                       "disclosed_quantity":dscqty,
                       "MktPro":"NA",
                       "price":prc,
                       "trigger_price":trgprc,
                       "product":product,
                       "is_amo":"NO"
                   }
            } 
    url = self.burl + "PlaceOrder"   
    response = requests.post(url,json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue


  def place_multi_order(self, order_list):
    l =order_list
    for i in range(len(l)):
      l[i]["exchange"]=l[i]["exchange"]
      l[i]["symbol"]=str(l[i]["ticker"])
      l[i]["quantity"]=str(l[i]["qty"])
      l[i]["product"]=l[i]["product"]
      l[i]["price"]= str(l[i]["price"])
      l[i]["transaction_type"]=l[i]["action"]
      l[i]["order_type"]=l[i]["ordertype"]
      l[i]["disclosed_quantity"]=l[i]["discqty"]
      l[i]["trigger_price"]=l[i]["trigprc"]
      l[i]["is_amo"]= "NO" 
      l[i]["ordersource"]="API"
      l[i]["stgy_name"]="stgname"
      l[i]["duration"]="DAY"
      l[i]["MktPro"]="NA"
      l[i]["user_apikey"]=l[i]["user_apikey"]
      l[i]["api_secret"]=l[i]["api_secret"]
      l[i]["order_refno"]="1"
    
             
        
    data = {
              "api_key": self.apikey,
              "api_secret": self.apisecret,
              "data":
                {
                   "orders": l
                }
            }
    print(data)     
    url = self.burl + "PlaceMultiOrder"        
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue          
    
  def place_bracket_order(self,ticker,exchange,action,ordertype,qty,dscqty,prc,trgprc,stoploss,squareoff,trailticks,strategy_name="Test Strategy"):
                            
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                  
                    "strg_name":strategy_name,
                    "symbol":ticker,
                    "exchange":exchange,
                    "transaction_type":action,
                    "duration":"DAY",
                    "order_type":ordertype,
                    "quantity":qty,
                    "disclosed_quantity":dscqty,
                    "MktPro":"NA",
                    "price":prc,
                    "trigger_price":trgprc,
                    "product":"OCO",
                    "stoploss": stoploss,
                    "squareoff":squareoff,
                    "trailing_ticks":trailticks
                }
        }
    url = self.burl + "PlaceBOOrder"
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue
      
      
     
  def place_option_order(self,spot,expiry,optiontype,action,ordertype,qty,product,strike,price=0,offset="10",trigprice=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
             "api_key":apikey,
             "api_secret":apisecret,
             "data":{ 
                      "stgy_name":"opt_ord",
                      "spot_sym":spot,
                      "expiry_dt":expiry,
                      "opt_type":optiontype,
                      "transaction_type":action,
                      "order_type":ordertype,
                      "quantity":qty,
                      "price":price,
                      "trigger_price":trigprice,
                      "product":product,
                      "strike_int":strike,
                      "offset":offset
                     
                    }
           }
    url = self.burl + "PlaceFOOptionsOrder"     
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue
  def modify_order(self,orderno,qty,ordertype=0,dscqty=0,prc=0,trigprice=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "strg_name":"Test Strategy",
                     "order_id":orderno,
                     "quantity":qty,
                     "order_type":ordertype,
                     "price":prc,
                     "trigger_price":trigprice,
                     "disclosed_quantity":dscqty
                  }
             }
    url = self.burl + "ModifyOrder"           
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue         

  def cancel_order(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "order_id":orderno
                   }
             }
    url = self.burl +"CancelOrder"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue        
              
  def profile(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"Profile"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                  

  def balance(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"Balance"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 

  def holdings(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"Holdings"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def order_book(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"Orders"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue       

  def order_history(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                   
                    "order_id":orderno
                    
                   }
             }
    url = self.burl +"OrderHistory"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def positions(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
         
             }
    url = self.burl +"Positions"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue             
                              
 
  def trade_book(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"Tradebook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                                         

  def feed(self,exchange,ticker,typ):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "exchange" : exchange,
                     "symbol": ticker,
                     "type" :typ,
                    }
             }
    url = self.burl +"Feed"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  def historical(self,exchange,ticker,interval,startdate,enddate):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "symbol":ticker,
                     "exchange":exchange,
                     "interval":interval,
                     "start_date":startdate,
                     "end_date":enddate,
                     "format":"json"
                    }
             }
    url = self.burl +"Historical"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  def security_info(self,exchange,ticker):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                       "exchange" :exchange,
                       "symbol" :ticker
                    }
             }
    url = self.burl +"SecurityInfo"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 









