#!/bin/bash

# Requires Ubuntu 20.04 (LTS) x64
# python 3.8 or 3.9 required

WORKDIR=~/work
PROJECT=qwizkool-django
PROJECT_DIR=$WORKDIR/$PROJECT
DJANGO_APP=qwizkoolweb
APPDIR=$PROJECT_DIR/$DJANGO_APP
GIT_USER=kgvinod

DBFILE=$APPDIR/db.sqlite3
SERVER_IP=0.0.0.0
SERVER_PORT=8080

function fresh() {
  if [ -d "$PROJECT_DIR" ]; then
    echo "$PROJECT_DIR exists."
    cd $PROJECT_DIR
    git status
    echo " "
    echo " "
    read -p "This will delete your project. Press any key to continue or CTRL-C to quit!"
  fi

  if [[ "$VIRTUAL_ENV" != "" ]]; then
    deactivate
  fi

  mkdir -p $WORKDIR
  cd $WORKDIR
  git clone git@github.com:$GIT_USER/${PROJECT}.git
  cd qwizkool-django/
  python3 -m venv .venv
  build
}

function clean() {

  if [[ "$VIRTUAL_ENV" == "" ]]; then
    source $PROJECT_DIR/.venv/bin/activate
  fi

  rm $DBFILE
  build
}

function build() {

  if [[ "$VIRTUAL_ENV" == "" ]]; then
    source $PROJECT_DIR/.venv/bin/activate
  fi

  # Install libs
  cd $PROJECT_DIR
  pip install -r requirements.txt
  cd qwizkool-nlp/
  pip install .

  # Migrate DB
  cd $APPDIR
  python manage.py makemigrations quiz
  python manage.py migrate

  # Run server
  run
}

function run() {  
  
  if [[ "$VIRTUAL_ENV" == "" ]]; then
    source $PROJECT_DIR/.venv/bin/activate
  fi
  
  cd $APPDIR
  python manage.py runserver $SERVER_IP:$SERVER_PORT
}

clean
