# NeoFi-PythonBackend
This is a repository which include the solution of Assessment for NeoFi Python Backend. Developed a RESTful API for a simple note-taking application. The API allows users to perform basic CRUD operations (Create, Read, Update, Delete) on notes.

### Setup
1. Create a virtual env using:
```
Python3 -m venv venv
```
2. Activate the virtual env using
Windows:
```
venv/Scripts/activate
```
Ubuntu
```
Source venv/bin/activate
```

3. Install go to the Project directory and install requirements.txt
```
pip install -r requirements.txt
```
### Development Server
1. Create migrations using
```
python manage.py makemigrations
```
2. Migrate the created migrations
```
python manage.py migrate
```
3. Run the server using command:
```
python manage.py runserver
```
Navigate to the following Endpoint, you will find the whole API documentation
```
http://127.0.0.1:8000/api/docs/
```

### Running the Test
Use the Command for running Test:
```
python manage.py test
```

***Cheers!!!***

