# Simple words similarity API

## Requirements
* python 2.7

## Important notes

In local environment the api is works without requesting access token for facility but in production is necessary that user follow step 7 and request a access token.

In production the endpoint /words/distance/ in body of request change word_1 and word_2 to word1 and word2.

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
		$ (env) pip install -r requirements.txt

4. Create a symbolic link to to offline documentation of api

		$ (env) ln -s swagger.local.json swagger.json (local)
		$ (env) ln -s swagger.production.json swagger.json (production)

or to production environment

    
       
5. Running migrations

		$ (env) python manage.py makemigrations
		$ (env) python manage.py migrate
       
6. Running the application

		$ (env) python manage.py runserver

By default django startup application in port 8000

7. Get access token for interacting with api, send credentials to endpoint bellow:

		[GET] http://localhost:8000/api/v1/auth/request_access/
		{
			"username": "someuser",
			"password: "yourpassword",
			"email": "youremail"
		}

If everthing is correct your should see the response like this:

		{
			"token":"some token"
		}
       
Now see the documentation and interact with API, append this entry in eache request:

        "Authorization": "Bearer <your_token>"


## Tests

For running tests running:

		$ python manage.py test
       
## Live demo

You can get your token in endpoint bellow:

		https://simple-words-api.herokuapp.com/api/v1/auth/request_access/
      
The complete documentation can be seen in:

		http://localhost:8000/api/v1/docs/ (Preferably)
Or

        https://simple-words-api.herokuapp.com/api/v1/docs/
