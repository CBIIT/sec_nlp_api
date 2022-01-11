
# SEC_NLP_API


## About this project

This api is a prototype used for creating a RESTful and Websocket request to process trail data and returning meaningful NCI c-codes.

## Getting Started

#### Required stack

 - [Python](https://www.python.org/) >= 3.8.12
 - [Redis](https://redis.io/) >= 4

#### Other Requirements

This project requires that you provide the database for the nlp.  This is created from the sec_poc repo under db_api_etl.  The SQLite db can be named anything you would like.  Just make sure you point config.py to the correct db.


### Setting up

Install the required libraries:
```
pip install -r requirements.txt
```
Create the nlp pickle:
```
flask init-nlp
```
Start flask:
```
python application.py
```