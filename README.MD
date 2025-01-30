# Password Manager
Development tools

* Django
* Django rest Framework

## How to run locally.

1. Clone the repository.
2. Enter in the folder
3. Create a enviroment with python 3.12.
4. Active the enviroment.
5. Install the dependencies.
6. Execute the env_gen 
7. Run the migrate
8. Run the project.



```
git clone git@github.com:ffabiorj/password-manager.git
cd caffeex
python3 -m venv .venv
sourch .venv/bin/activate
pip install -r requirements.txt
python env_gen.py
python manage.py migrate
python manage.py runserver

```

## Endpoints of api

Endpoint for doc api.
http://localhost:8000/redoc/

### Endpont to create a login.
Method post localhost:8000/api/v1/register/
Body
```
{
    "username": "teste",
    "email": "teste@teste.com",
    "password": "teste"
}
```
### Endpoint to generate a token login.
Method post localhost:8000/api/v1/api/token

Body
```
{
    "username": "teste",
    "password": "teste"
}
```
### Endpoint to create a password entry
Method post localhost:8000/api/v1/passwords/
Body
{
    "name": "test8",
    "icon": "https://example.com/new-icon.png",
    "notes": "Updated notes",
    "url": "https://new-example.com",
    "username": "newuser",
    "password": "newpassword",
    "user": 1
}

### To access these endpoints you need to send a token authorization "Bearer token"
## Endpoint to get all passwords 
Obs: In this method you can use the query string for search a entry password e.g passwords/?search=<name>.
This method has pagination, each page has five entries, to see other entries, use passwords/?page=2
Method get localhost:8000/api/v1/passwords/

Response:

```
[
    {
        "id": 6,
        "name": "test8",
        "icon": "https://example.com/new-icon.png",
        "notes": "Updated notes",
        "url": "https://new-example.com",
        "username": "newuser",
        "password": "newpassword",
        "user": 1
    }
]

```
### Endpoint to get a detail about a password.
Method get localhost:8000/api/v1/password/\<int\>

Response
```
{
    "id": 6,
    "name": "test8",
    "icon": "https://example.com/new-icon.png",
    "notes": "Updated notes",
    "url": "https://new-example.com",
    "username": "newuser",
    "password": "newpassword",
    "user": 1
}
```

### Endpoint to update a password.
Method put localhost:8000/api/v1/password/\<int\>

Body
```
{
    "name": "test8",
    "icon": "https://example.com/new-icon.png",
    "notes": "Updated notes",
    "url": "https://new-example.com",
    "username": "newuser",
    "password": "newpassword",>
}
```

### Endpoint to delete a password.
Method delete localhost:8000/api/v1/password/\<int\>

## Execute tests
#### To see all the behaviors of this api, look at the test file in app passwords folder.
1. To test the api

```
python manage.py test
```
