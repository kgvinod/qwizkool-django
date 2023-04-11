# qwizkool-django

Use python 3.9

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

Apache wsgi configuration in /atc/apache2/apache2.conf
```
WSGIScriptAlias /qwizkool /home/vinod/work/deploy/qwizkool-django/qwizkoolweb/qwizkoolweb/wsgi.py
#process-group=example.com
WSGIPythonHome /home/vinod/work/deploy/qwizkool-django/.venv/
WSGIPythonPath /home/vinod/work/deploy/qwizkool-django/qwizkoolweb/
#WSGIDaemonProcess example.com python-home=/home/vinod/work/qwizkool-django/.venv/ python-path=/home/vinod/work/qwizkool-django/qwizkoolweb/
#WSGIProcessGroup example.com

<Directory /home/vinod/work/deploy/qwizkool-django/qwizkoolweb/qwizkoolweb/>
<Files wsgi.py>
        Require all granted
        #Order deny,allow
        #Allow from all
</Files>
</Directory>
```
Make the entire project read/write using chmod -R 777 . The sqlite db needs to be writable by the www user.
Install libapache2-mod-wsgi-py3 (if libapache2-mod-wsgi is installed, remove! This works only with python 2)

Update : It does not appear that the entire project needs to be made read/write. Only the db forler and the db file itself
chmod 777 qwizkool-django/qwizkoolweb
chmod 777 qwizkool-django/qwizkoolweb/db.sqlite3

Digital Ocean Notes
 - Spacy model pip install did not work in Digital Ocean. Instead, run the following in venv:
    - python -m spacy download en_core_web_sm
 - The server IP needs to be added to Adjango's LLOWED_HOSTS lists
