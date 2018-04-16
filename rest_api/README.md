* Install the required dependencies:

    `pip install -r requirements.txt`

* (Windows) Run the web-server:

    `waitress-serve --port=8000 app:api`
* (OSX/Linux) Run the web-server:

    `gunicorn app:api --reload --port=8000`

* Open the web-browser and enter:

    `http://localhost:8000/persons/`
