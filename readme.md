# How to get the flask app running

## Folder structure
* Create a folder named studio2-flask
* Create a worldfacts folder within this folder
* Clone this repository to the worldfacts folder
    * _cd worldfacts_
    * _git clone https://github.com/Aora13373/No-Name.git ._

## Virual environment setup
* From the studio2-flask folder, create a virtual environment and activate it
    * _pip install virtualenv_
    * _python -m venv venv_
    * _venv\Scripts\activate_
* Install flask with the command _pip install flask_
* Common dependencies to install: 
    * _pip install pandas_
    * _pip install pymongo_
    * _pip install dnspython_


## Running the app (windows)
* From the studio2-flask folder, enter the following commands
* _set FLASK\_APP=worldfacts_ 
* _set FLASK\_ENV=development_ 
* _flask run_

Install any missing dependencies depending on error message
