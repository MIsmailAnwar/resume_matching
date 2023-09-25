# resume_matching
Resume matching

## Setup
cd to you working directory

> cd to-your-working-directory

create a virtual environment

> python -m env venv

activate the python venv

> source venv/Scripts/activate.bat

install required python packages

> pip install -r requirements.txt

> python -m spacy download en_core_web_sm

make django migrations

> py manage.py makemigrations

> py manage.py migrate

run python script to import data

> python import_resumes.py

run django 

>py manage.py runserver
