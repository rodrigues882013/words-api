# Simple words similarity API

## Requiremnts
* python 2.7

## Instructions

1. Clone repository

       $ git clone https://github.com/rodrigues882013/words-api.git
       $ cd words-api/
 
2. Install Virtualenv
      
       $ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
       $ tar xvfz virtualenv-1.9.tar.gz
       $ cd virtualenv-1.9
       $ python virtualenv.py /path/to/virtualenv/env

3. Switch to new virtualenv created and install requirements

       $ source /path/to/virtualenv/env/bin/active
       $ pip install -r requirements.txt

4. Running migrations

       $ python manage.py makemigrations
       $ python manage.py migrate
       
5. Running the application

       $ python manage.py runserver
By default django startup application in port 8000

6. Get access token for interacting with api, send credentials to endpoint bellow:

       [GET] http://localhost:8000/api/v1/auth/request_access/
       {
            "username": "someuser",
            "password: "yourpassword",
            "email": "youremail"
       }
If everthing is correct your should see the response like this:

       {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE0ODgyMDM5ODh9.I4e1RE3B3GP7ptE_5ZBPMU_d-ulXNBRW5JXGFbGZvOg",
       }
       
Now see the documentation and interact with API


## Tests

For running tests running:

       $ python manage.py test
       
## Live demo

You can get your token in endpoint bellow:

      https://simple-words-api.herokuapp.com/api/v1/auth/request_access/
      
The complete documentation can be see in:

      https://simple-words-api.herokuapp.com/api/v1/docs/
