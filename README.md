# Knowledge Center API

## Tech stack

* Database - SQLite
* Web Framework - Django
* Programming language - Python
* API Documentation - Drf Yasg

## Setup Instructions
__Steps__

1. Django Environment Setup
    
        virtualenv -p python3 env_name 
        
        source env_name/bin/activate
        
        pip install -r requirements.txt
        
2. Run Server
    
        python manage.py migrate            # to migrate all the migrations
                        
        python manage.py runserver          # to run the server
        
        The server will start at localhost:8000
        
3. Setup OAuth
 
    Open the following Url and Register a new OAuth Application
   
        localhost:8000/o/applications/register
        
    Enter Application name and Choose Client type as `Confidential` and Authorization grant type as `Resource owner password-based`  
        
    Copy the client id, client secret and Save the application 

4. API Docs

    API documentation can be accessed at 
    
        localhost:8000/docs/ 
        
5. Unit tests

        python manage.py test
        
## Tables

1. User
2. Category
3. Knowledge Base
4. Document File