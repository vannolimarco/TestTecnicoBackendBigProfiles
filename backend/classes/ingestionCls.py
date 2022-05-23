# -----------------------------------------------------------
# Class ingestion api method
#
# (C) 2022 Marco Vannoli, Rome, Italy
# email marcovannoli@hotmial.it
# -----------------------------------------------------------

from datetime import datetime
from sqlite3 import Date
from pydantic import BaseModel

# Data Structure of input for method "ingest" :
# Example:
# {
# Payload: payload ingested as input
# Key: key ingested as input
# }

class InputIngestion(BaseModel):
        key: int | None = None 
        payload: str | None = None 


# Data Structure to ingest into Dtabase (MongoDB) :
# Example:
# {
# Creation_datetime: date of creation (y/m/d h/m/s)
# Payload: payload ingested as input
# Response_time: time of response of call
# Response_code: response code
# Key: key ingested as input
# }

class DataDB(BaseModel):
    Key: int | None = None
    Creation_datetime: datetime | None = None
    Payload: str | None = None
    Response_time: int | None = None
    Response_code: int | None = None



    