lobbypy-heroku
==============

*A game lobby system to run on Heroku*

lobbypy-heroku is a web based TF2 lobby system built on Flask and Heroku.

Requirements
------------

* [Python 2.7](http://www.python.org/download/)
* [virtualenv](http://pypi.python.org/pypi/virtualenv/)
* [pip](http://pypi.python.org/pypi/pip)
* [Heroku Toolbelt](https://toolbelt.heroku.com/)

Developing
----------

### Setup ###

* Clone the repository

        git clone git@github.com:TronPaul/lobbypy-heroku.git
        cd lobbpy-heroku

* Create the virtualenv

        virtualenv venv

* Activate the virtualenv

        source venv/bin/activate

* Install the required Python packages

        pip install -r requirements.txt

* Add the needed environment variables to `.env`
    * `SESSION_KEY` - session key for Flask's cookie
    * `DEV_DATABASE_URI` - SQLAlchemy URI for the development database
    * `STEAM_API_KEY` - Steam API key

 The file should look something like `env.sample`

### Usage ###

Use `foreman` from the Heroku Toolbelt to run commands and start the
server with the heroku environment.  See the
[man page](http://ddollar.github.com/foreman/) for documentation.
