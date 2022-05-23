
# -----------------------------------------------------------
# File to execute test 
#
# (C) 2022 Marco Vannoli, Rome, Italy
# email marcovannoli@hotmial.it
# -----------------------------------------------------------

from cgi import test
from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from requests import TooManyRedirects,HTTPError
import time
import json
import dateutil.parser as parser
from database import get_database,save_to_database
from config import get_config
from fastapi.testclient import TestClient
from main import app
from classes.ingestionCls import InputIngestion, DataDB
from classes.apiCls import OutputApi
from classes.retrieveCls import OutputRetrive, OutputValue, OutputLogs


client = TestClient(app)

# get data of database Mongo DB
data = get_config()


# get database
db = get_database()

# collection name
collection_name = db[data["collection"]]


# call ingest api method
def test_ingest_api(body):
    response = client.post("/api/v1/ingest",headers={"x-api-key": "BigProfiles-API"}, json=body)
    return response

# call retrive api method
def test_retrieve_api(date_from,date_to):
    response = client.get("/api/v1/retrieve/"+date_from+"/"+date_to,headers={"x-api-key": "BigProfiles-API"})
    return response.json()


# too test ingest from client
body = {"key": 2, "payload": "Stringa Esempio "}
json_response = test_ingest_api(body)
print('Test Api Ingestion response : {}'.format(json_response.status_code))

# too test retrive from client
date_from = "2022-05-23 14:40:00"
date_to =  "2022-05-23 14:50:00"
json_response = test_retrieve_api(date_from,date_to)
print('Test Api Retrieve response : {}'.format(json_response))

