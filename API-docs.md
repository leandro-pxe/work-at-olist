# Call register
* URL: /api/calls
* Method: POST
* Object description:
    - type
        
        Description: Indicate if the call starts or ends.
        
        Data Type: Char
        
        Formar: START or END
    
    - date_register
        
        Description: Registration date and time
        
        Data Type: DateTime
        
        Formar: YYYY-MM-DDThh:mm:ssZ
    
    - call_id
        
        Description: Call ID (must be the same to start and end calls)
        
        Data Type: Char
        
        Formar: numeric
    
    - source
        
        Description: Source phone number
       
        Data Type: Char
       
        Formar: AAXXXXXXXXX or AAXXXXXXXX
    
    - destination
       
        Description: Destination phone number
      
        Data Type: Char
      
        Formar: AAXXXXXXXXX or AAXXXXXXXX
    
    Start calls – All fields are required.
    
    End calls – type, date_register and call_id are required.


# Call bill
* URL: /api/bill
* Method: GET
* Object description:
    - phone
        
        Description: Source phone number (required).
        
        Data Type: Integer
        
        Formar: AAXXXXXXXXX or AAXXXXXXXX
    
    - period
        
        Description: Month and year (optional)
        
        Data Type: Char
        
        Formar: MM/YYYY
    
	
   Returns **destination phone number**, **call start date**, **call start time**, 
   **call duration** and **call price** for each call in the period. 
   In case of no period, the last month is the reference.
