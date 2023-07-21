Beer Depot CLI App

## Description
Small CLI application that allows users to browse the inventory of beers currently available at any given store. 

## Users can:
- Filter through the beers by name of beer, brewery, and style of beer

Wireframe template:
https://wireframe.cc/ODGCKS


## Instructions

Fork and clone the repository to your local machine and open the files up in your code viewer.

In your terminal run: 

`pipenv install`

`pipenv shell`

Then navigate to the lib/db directory by typing in:

`cd lib/db`

Next run:

`alembic revision --autogenerate -m "test"`

`alembic upgrade head`

`python seed.py`

To test the app, navigate back to the /lib folder by entering

`cd ..` and running `python main.py`


### Libraries and Tools used ###

PrettyTable - https://pypi.org/project/prettytable/
Click - https://click.palletsprojects.com/en/8.1.x/
Text to ASCII Art Generator - http://patorjk.com/software/taag/
Faker - https://faker.readthedocs.io/en/master/index.html

