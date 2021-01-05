# qwizkool-django
```
  git clone git@github.com:kgvinod/qwizkool-django.git
  cd qwizkool-django/
  git clone git@github.com:kgvinod/qwizkool-nlp.git
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  cd qwizkool-nlp/
  pip install .
  cd ..
  cd qwizkoolweb/
  python manage.py makemigrations quiz
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8080
```  
