# URL Shortner

## Getting Started

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

### Linux
```bash
$ virtualenv project-env
$ source project-env/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

### Windows
```bash
$ python -m venv project-env
$ .\project-env\Scripts\activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

#### If the project doesn't run with requirements.txt install optional_req.txt 
```bash
$ pip install -r optional_req.txt
```


## Admin User

* First set up and superuser account where the user can maintain the system 
```bash
$ python manage.py create superuser
```
enter the credentials you want to set up and then , user credentials to login to 
http://localhost:8000/admin

* After logging as a superuser, go to the url: http://localhost:8000/admin/sites/site/add/ and add localhost:8000 in domain name and localhost in display name