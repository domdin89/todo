## Create a virtual evironment
`` python3 -m venv project_env ``

## Check with ls that is created the folder
`` ls ``

## Activate virtual environment
`` source project_env/bin/activate ``

## Install requirements
`` pip install -r requirements.txt ``

## Migrate Db
`` python3 manage.py makemigrations ``
`` python3 manage.py migrate ``  

## Start the project
`` python3 manage.py runserver ``

## Create superuser

## All in one Mac

`` python3 -m venv project_env && source project_env/bin/activate &&  pip install -r requirements.txt ``

`` python3 -m venv project_env && source project_env/bin/activate &&  pip install -r requirements.txt && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver ``