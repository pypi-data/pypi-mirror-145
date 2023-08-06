
Metadata-Version: 2.1

Name: Algomojo-kambala

Version: 1.0

Summary: A functional python wrapper for  trading api

Home-page: 

Author: Algomojo

Author-email: support@algomojo.com

License: MIT

Description: 
        ## ABOUT
        A functional python wrapper for Algomojo-kambala trading api.
        It is a python library for the [Algomojo Free API + Free Algo Trading Platform ](https://algomojo.com/). 
        It allows rapid trading algo development easily, with support for both REST-API interfaces. 
        Execute Orders in Reatime, Modify/Cancel Orders, Retrieve Orderbook, Tradebook, Open Positions, 
		Squareoff Positions and much more functionalities. 
        For more details of each API behavior, Pease see the Algomojo API documentation.
        
        
        ## License
        
         Licensed under the MIT License.

        
        ## Documentation
        [Algomojo Rest API documentation ](https://algomojo.com/docs)
        
        
        
        
        ## Installation
        Install from PyPI
        
        	pip install algomojo-kambala
        
        Alternatively, install from source. Execute setup.py from the root directory.
        python setup.py install
        
        Always use the newest version while the project is still in alpha!
        
        
        ## Usage Examples
        In order to call Algomojo trade API, you need to sign up for an trading account with one
of the partner broker and obtain API key pairs and enjoy unlimited access to the API based trading.
        Replace api_key and api_secret_key with what you get from the web console.
        
        
        
        
        ## Getting Started
        
        After downloading package import the package and create the object with api credentials
        
        
        	from algomojo import kambala
        
        
        
        
        
        ## Creating  Object
        
        For creating an object there are 3 arguments which would be passed
        
                 api_key : str
                     User Api key (logon to algomojo account to find api credentials)
                 api_secret : str
                     User Api secret (logon to algomojo account to find api credentials)
                 Broker : str
                     This takes broker it generally consists 2 letters , 
					 EX:tradejini-->tc, firstock-->fs
        
        Sample:
        	
        	at=kambala.api(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        		    api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                     broker="tc")
        
        
        
        
        
        
        ## Using Object Methods
        obj.method(mandatory_parameters)  or obj.method(madatory_parameters+required_parameters)
        
        
        # Avaliable Methods
        	
        ### 1. place_order:  
        
        		Function with mandatory parmeters: 
        				place_order(client_id,exchange,ticker,qty,action,ordertype,product)
        		
        		Function with all parametrs:       
        				place_order(client_id,exchange,ticker,qty,action,ordertype,
						            product,prc,dscqty,trigprc)
                 	 
                        Sample :        
        				at.place_order(client_id="GH1456",exchange="NSE"
        					       ticker="SBIN-EQ",qty="50"
        					       action="B",ordertype="MKT"
        					       product="C")   
        ### 2. place_multi_order:
        
        		place_multi_order(order_list)

	           Sample order_list:(tradejini cube:) 
		             [{"client_id":"TM0554","user_apikey":"xxxxxxxxxxxxxxxxxxxxxx",
					 "api_secret":"xxxxxxxxxxxxxxxxxxxxxxxxx","ticker":"INFY-EQ","exchange":"NSE",
					 "action":"B","qty":"1","price":"500","ordertype":"MKT",
					 "product":"C","trigprc":"0","trigprice":"0",
                     "dscqty":"0","bookprofit":"0","bookloss":"0","trailprice":"0"},
                     {"client_id":"TM0554","user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
					 "api_secret":"xxxxxxxxxxxxxxxxxx",
                     "ticker":"BHEL-EQ","exchange":"NSE","action":"B","qty":"10","price":"200","ordertype":"MKT",
					 "product":"C","trigprice":"0","dscqty":"0","bookprofit":"0","bookloss":"0","trailprice":"0",}]

                Sample order_List:(first stock):
				    [{"client_id":"RR0884","user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxxxx",
					"api_secret":"xxxxxxxxxxxxxxxxxxxxxxxxxxx","ticker":"INFY-EQ",
					"exchange":"NSE","action":"B","qty":"1","price":"500","ordertype":"MKT",
					"product":"C","trigprc":"0","discqty":"0"},
		           {"client_id":"RR0884","user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
				   "api_secret":"xxxxxxxxxxxxxxxxxxxxxxxxxx","ticker":"INFY-EQ",
				   "exchange":"NSE","action":"B","qty":"10","price":"200","ordertype":"MKT",
				   "product":"C","trigprc":"0","discqty":"0"}]
	            Sample function call:  
	             	ab.place_multi_order(order_list)
        
        ### 3. place_option_order
        
        		Funtion with mandatory parameters:  
        			     place_option_order(client_id,spot,expiry,action,
						                optiontype,ordertype,qty,strike)
        		Function with all parameters: 
        		 
        		            place_option_order(client_id,spot,expiry,action,
							                  optiontype,ordertype,qty,strike,
							                   price,product,trigprice,offset)
        		
        		Sample :          
        		        at.place_option_order(client_id="RR0884",spot="NIFTY",
						                     expiry="24FEB22",action="B",
						                      optiontype="C",ordertype="MKT",
											  qty="50",strike="100")
        
        		
        ### 4. modify_order:
        
        		Funtion with mandatory parameters:  
        			     	modify_order(client_id,orderno,qty,prc)
        		
        		Function with all parameters:
        		 	      	modify_order(client_id,orderno,exchange,ticker,ordertype,qty,prc,trigprice)
        		
        		Sample for tradejini: `		   
        				at.modify_order(client_id="DF4569",orderno="1457896512",
						        qty="70",prc="600")
        		
        		
        		
        
        
        
        ### 5. cancel_order
        
        		Funtion with mandatory parameters:   
        				cancel_order(client_id,orderno)
        
        		Function with all parameters:          
        		
        				cancel_order(client_id,orderno)
        
        		Sample:             
        				at.cancel_order(uid="RA4456",orderno="4567891523")

        
        		
        
        ### 6. user_details:
        
        		Funtion with mandatory parameters:   
        					user_details:(client_id)
        					
        		Function with all parameters:        
        					user_details:(client_id)
        					
        		Sample:                              
        					at.user_details(client_id='AB1234')
        					             
        
        ### 7. limits
        
        
        		Funtion with mandatory parameters:   
        					limits(client_id)
        					
        		Function with all parameters:        
        					limits(client_id)
        					
        	        Sample:                              
        					at.limits(client_id='AB1234')
        		                                    
        
        
        
        
        
        ### 8. holdings: 
        
        		Funtion with mandatory parameters:   
        					holdings(client_id,prd)
        					
        		Function with all parameters:       
        					holdings(client_id,prd)
        					
        		Sample:                              
        					at.holdings(uid='AB1234',prd="C")
        
        
        
        ### 9. order_book:
        
        
        		Funtion with mandatory parameters:   
        					order_book(client_id)
        		
        		Function with all parameters:        
        					order_book(client_id,actid)
        					
        		Sample:                             
        					at.order_book(client_id='AB1234')
        
        
        
        
        
        ### 10. Single_hist:
        
        
        		Funtion with mandatory parameters:   
        					Single_hist(client_id,orderno))
        					
        		Function with all parameters:        
        					Single_hist(client_id,orderno))
        					
        		Sample:                              
        					at.order_history(client_id='AB1234',
        							 orderno='201109000000025')
        
        
        
        
        ### 11. position_book
                
             	Funtion with mandatory parameters:   
        					position_book(client_id)
        					
        		Function with all parameters:        
        					position_book(client_id)
        					
        		Sample:                              
        					at.position_book(client_id='AB1234')
        
                    
        					
        
        		
        		
        		
        
        
        
        
        ### 12. trade_book
                
             	Funtion with mandatory parameters:   
        					trade_book(client_id)
        					
        		Function with all parameters:        
        					trade_book(client_id)
        					
        		Sample:                              
        					at.trade_book(client_id='AB1234')
        
        
        
        ### 13.  get_quotes:
                
             	Funtion with mandatory parameters:   
        					get_quotes(client_id,exchange,token)
        					
        		Function with all parameters:        
        					get_quotes(client_id,exchange,token)
        					
        		Sample:                              
        					at.get_quotes(cleint_id='AB1234',
							              exchange="NSE",
							              token="2645")

        ### 14.  show_quotes:
                
             	Funtion with mandatory parameters:   
        					      show_quotes(client_id,exchange,stext)
        					
        		Function with all parameters:        
        					      show_quotes(client_id,exchange,stext)
        					
        		Sample:                              
        					at.show_quotes(cleint_id='AB1234',exchange="NSE",
							 "stext":"RELIANCE-EQ")

        ### 15.exit_SNO_order:
                 Funtion with mandatory parameters: 
                                     exit_SNO_order(client_id,orderno,product)
                 Sample:
                              at.exit_SNO_order(client_id="xxxx",orderno="516549493454",
                                           product="H")                    
        
        
    
         
        