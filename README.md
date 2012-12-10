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
    * SESSION\_KEY - session key for Flask's cookie
    * DEV\_DATABASE\_URI - SQLAlchemy URI for the development database

 The file should look something like `env.sample`
