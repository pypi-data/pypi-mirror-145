import json
import requests

class api:
  def __init__(self,apikey,apisecret,broker,version="1.0"):
     self.apikey=apikey 
     self.apisecret=apisecret
     self.burl = "https://" + broker + 'api.algomojo.com/' + str(version) + '/'
  def place_order(self,client_id,exchange,ticker,qty,action,ordertype,product,price="0",dscqty="0",trigprice="0",bookprofit="0",bookloss="0",trailprice="0"):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "strg_name": "Test Strategy",
                     "uid":client_id,
                     "actid":client_id,
                     "exch":exchange,
                     "tsym":ticker,
                     "qty":qty,
                     "prc":str(price),  
                     "trgprc":str(trigprice),
                     "dscqty":str(dscqty),
                     "prd":product,
                     "trantype":action,
                     "prctyp":ordertype,
                     "ret":"DAY",
                     "remarks":"",
                     "ordersource":"API",
                     "bpprc":str(bookprofit),
                     "blprc":str(bookloss),
                     "trailprc":str(trailprice),       
                     "amo":"NO",
                    }
            } 
    url = self.burl + "PlaceOrder"   
    response = requests.post(url,json.dumps(data), headers={'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return jsonValue


  def place_multi_order(self, order_list):
    l =order_list
    for i in range(len(l)):
      l[i]["user_apikey"]=l[i]["user_apikey"]
      l[i]["api_secret"]=str(l[i]["api_secret"])
      l[i]["uid"]=str(l[i]["client_id"])
      l[i]["actid"]=l[i]["client_id"]
      l[i]["tsym"]= str(l[i]["ticker"])
      l[i]["exch"]=l[i]["exchange"]
      l[i]["trantype"]=l[i]["action"]
      l[i]["prctyp"]=l[i]["ordertype"]
      l[i]["qty"]=l[i]["qty"]
      l[i]["dscqty"]=l[i]["dscqty"]
      l[i]["AMO"]= "NO" 
      l[i]["ordersource"]="API"
      l[i]["remarks"]=""
      l[i]["strg_name"]="stgname"
      l[i]["ret"]="DAY"
      l[i]["MktPro"]="NA"
      l[i]["prc"]=l[i]["price"]
      l[i]["trgprc"]=l[i]["trigprice"]
      l[i]["prd"]=l[i]["product"]
      l[i]["bpprc"]=l[i]["bookprofit"]
      l[i]["blprc"]=l[i]["bookloss"]
      l[i]["trailprc"]=l[i]["trailprice"]
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
    
    jsonValue = response.json()
    print(jsonValue)
    return jsonValue          
   

  def place_option_order(self,client_id,spot,expiry,action,optiontype,ordertype,qty,strike,price=0,product='C',trigprice=0,offset=1):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
             "api_key":apikey,
             "api_secret":apisecret,
             "data":{ 
                     "strg_name":"Test Strategy",
                     "uid":client_id,
                     "spot_sym":spot,
                     "expiry_dt":expiry,
                     "Ttranstype":action,
                     "opt_type":optiontype,
                     "prctyp":ordertype,
                     "qty": qty,
                     "Price":str(price),
                     "TrigPrice":str(trigprice),
                     "Pcode":product,
                     "strike_int":str(strike),
                     "offset":offset
                     
                    }
           }
    url = self.burl + "PlaceFOOptionsOrder"     
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue
  def modify_order(self,client_id,orderno,exchange=0,ticker=0,ordertype=0,qty=0,prc=0,trigprice=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "strg_name": "Test Strategy", 
                    "uid":client_id,
                    "tsym":str(ticker),
                    "exch":str(exchange),
                    "prctyp":str(ordertype),
                    "qty ":str(qty),
                    "ret":"DAY",
		                "norenordno":orderno,
		                "prc":str(prc),
		                "trgprc":str(trigprice)
                  }
             }
    url = self.burl + "ModifyOrder"           
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue         

  def cancel_order(self,client_id,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "norenordno":orderno,
                   }
             }
    url = self.burl +"CancelOrder"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue        
              
  def user_details(self,client_id):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    
                   }
             }
    url = self.burl +"UserDetails"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                  

  def limits(self,client_id):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id
                    
                   }
             }
    url = self.burl +"Limits"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 

  def holdings(self,client_id,product):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id,
                    "prd":product,
                    
                   }
             }
    url = self.burl +"Holdings"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def order_book(self,client_id):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id
                    
                   }
             }
    url = self.burl +"OrderBook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue       

  def Single_hist(self,client_id,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id,
                    "norenordno":orderno
                    
                   }
             }
    url = self.burl +"SingleOrdHist"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def position_book(self,client_id):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id,
                    
                    
                   }
             }
    url = self.burl +"PositionBook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue             
                              
 
  def trade_book(self,client_id):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id,
                    
                    
                   }
             }
    url = self.burl +"TradeBook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                                         

  def get_quotes(self,client_id,exchange,token):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id,
                    "exch":exchange,
                    "token":token
                    
                    }
             }
    url = self.burl +"GetQuotes"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  def show_quotes(self,client_id,exchange,stext):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "uid":client_id,
                    "actid":client_id,
                    "exch":exchange,
                    "stext":stext
                    
                    }
             }
    url = self.burl +"ShowQuotes"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 

  def exit_SNO_order(self,client_id,orderno,product):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "norenordno":orderno,
                    "prd" : product,
                    "uid":client_id
                   }
                 }
    url = self.burl + "ExitSNOOrder"     
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue





