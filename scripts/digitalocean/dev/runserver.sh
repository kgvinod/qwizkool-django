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

  cd $HOME

  if [ -d "$PROJECT_DIR" ]; then
    echo "$PROJECT_DIR exists."
    cd $PROJECT_DIR
    git status
    echo " "
    echo " "
    read -p "This will delete your project. Press any key to continue or CTRL-C to quit!"
    rm -rf $PROJECT_DIR
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
  pip install wheel
  pip install --upgrade setuptools
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


PS3='Please enter your choice: '
options=("run" "build" "clean" "fresh")
select opt in "${options[@]}"
do
    case $opt in
        "run")
            echo "Running the server"
	    run
            ;;
        "build")
            echo "Building and running the server"
	    build
            ;;
        "clean")
            echo "Cleaning, building and running the server"
	    clean
            ;;
        "fresh")
            echo "Checking out, cleaning, building and running the server"
	    fresh
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

