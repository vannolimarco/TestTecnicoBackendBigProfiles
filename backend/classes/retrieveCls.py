# -----------------------------------------------------------
# Class retrive api method
#
# (C) 2022 Marco Vannoli, Rome, Italy
# email marcovannoli@hotmial.it
# -----------------------------------------------------------

from datetime import datetime
from pydantic import BaseModel

# Data Structure of output for logs "retrive" :
# Example:
# {
# Creation_datetime: date of creation (y/m/d h/m/s)
# Payload: payload ingested as input
# Response_time: time of response of call
# Response_code: response code
# Key: key ingested as input
# }

class OutputLogs(BaseModel):
    key: int | None = None
    creation_datetime: str | None = None
    payload: str | None = None
    response_time: int | None = None
    response_code: int | None = None


# Data Structure of output for values "retrive" :
# Example:
# {
# key: Key aggregate
# total_response_time_ms: total response time 
# total_requests: total request
# total_errors: total error code
# creation_datetime:  date aggregate
# }

class OutputValue(BaseModel):
        key: int | None = None 
        total_response_time_ms: int | None = None,
        total_requests: int | None = None,
        total_errors: int | None = None,
        creation_datetime: datetime | None = None


# Data Structure of entire final object "retrive" :
# Example:
# {
# values: values aggregate
# logs: logs aggregate 
# }

class OutputRetrive(BaseModel):
        values: list | None = None 
        logs: list | None = None






    