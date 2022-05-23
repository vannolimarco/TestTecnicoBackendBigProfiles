
# -----------------------------------------------------------
# API of the project (main)
# To Rune : cd ../backend/ -> run into terminal : uvicorn main:app --reload
# (C) 2022 Marco Vannoli, Rome, Italy
# email marcovannoli@hotmial.it
# -----------------------------------------------------------

from cgi import test
from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, Header
from pydantic import BaseModel
from requests import TooManyRedirects, HTTPError
import time
import dateutil.parser as parser
import json
from random import randint, randrange
from database import find_query, get_database, save_to_database, aggregation_collection
from config import get_config
from classes.ingestionCls import InputIngestion, DataDB
from classes.apiCls import OutputApi
from classes.retrieveCls import OutputRetrive, OutputValue, OutputLogs


# get json of config: name of database, connection string, name of collection
data = get_config()

# initialize app
app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}


@app.post("/api/v1/ingest")
async def ingestion(ingestionInput: InputIngestion, x_api_key: str | None = Header(default=None, x_api_key="")):

    # create output structure : {status_code: <CODE>, message: <STRING>}
    output = OutputApi()

    # generate number from 10 ms to 50 ms
    responseRandomTime = randint(10, 50)

    # response after random number generated
    time.sleep(responseRandomTime/1000)

    # start cycle and return response (managening of error according to json)
    try:
        # if the input is valid and the "x_api_key" is correct
        if x_api_key == "BigProfiles-API":
            # if the input is not valid
            if ingestionInput is None or (ingestionInput.key < 1 or ingestionInput.key > 6) or (ingestionInput.payload == ''):
                output.status_code = 422
                output.message = 'Validation Error'
                return output
            else:
                # generate 10% for Error: return Error Code 500
                responseRandomError = randrange(0, 100, 10)
                # create instance of Database MongoDB
                # (see config file)
                db = get_database()
                # collection name
                collection_name = db[data["collection"]]
                # the object (class) to save data into Database
                outputDB = DataDB()
                if responseRandomError == 10:  # 10% probability
                    outputDB.Response_code = 500   # error
                else:
                    outputDB.Response_code = 200   # success

                outputDB.Key = ingestionInput.key
                outputDB.Payload = ingestionInput.payload
                outputDB.Creation_datetime = datetime.today().replace(microsecond=0)
                outputDB.Response_time = responseRandomTime

                # creation of Json Object (Bjson) to save it into MongoDB
                # starting from class "InputIngestion"
                dataIngest: InputIngestion = {
                    "Key": outputDB.Key,
                    "Payload":  outputDB.Payload,
                    "Creation_datetime": outputDB.Creation_datetime,
                    "Response_time": outputDB.Response_time,
                    "Response_code": outputDB.Response_code
                }

                # insert into collection the new record
                save_to_database(collection_name, dataIngest)

                # set the response
                if responseRandomError == 10:
                    output.status_code = outputDB.Response_code
                    output.message = "Error 500"
                else:
                    output.status_code = outputDB.Response_code
                    output.message = "Ingestion Complete"

                # return the response of api ingestion
                return output
        else:
            # otherwise not Authorized
            output.status_code = 401
            output.message = 'Not Authorized'
            return output
    except TooManyRedirects:
        raise HTTPException(status_code=404,
                            detail="Many Redirects")
    except HTTPError:
        raise HTTPException(status_code=500,
                            detail="Server Error 500")


@app.get("/api/v1/retrieve/{date_from}/{date_to}")
async def retrieve(x_api_key: str | None = Header(default=None, x_api_key=""), date_from: str | None = Header(default=None), date_to: str | None = Header(default=None)):
    # create output structure : {status_code: <CODE>, message: <STRING>}
    output = OutputApi()

    try:
        # if the input is valid and the "x_api_key" is correct
        if x_api_key == "BigProfiles-API":

            if date_from == '' or date_to == '':
                output.status_code = 422
                output.message = 'Validation Error'
                return output
            else:

                # create instance of Database MongoDB
                # (see config file)
                db = get_database()
                # collection name
                collection_name = db[data["collection"]]

                # elaborate the date (ISO FORMAT)
                date_from_iso = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
                date_to_iso = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
                
                field_to_sort = "Creation_datetime"
                limit=10

                # take last 10 logs for temporal window : date from/to
                # limit of logs  10
                # order desc for date
                last_10_logs_query = [{
                        "$set":
                        {
                            "_id": 0,
                            "year": {"$year": "$Creation_datetime"},
                            "month": {"$month": "$Creation_datetime"},
                            "day": {"$dayOfMonth": "$Creation_datetime"},
                            "hour": {"$hour": "$Creation_datetime"},
                            "minuts": {"$minute": "$Creation_datetime"}
                        },

                    },
                    {
                        "$set": {
                            "dateNotSeconds": {"$concat": [{"$toString": "$year"}, "-", {"$toString": "$month"}, "-", {"$toString": "$day"}, " ", {"$toString": "$hour"}, ":", {"$toString": "$minuts"}, ":00"]}
                        }
                    },
                    {"$match":
                     {"$and": [{"year": {"$gte": date_from_iso.year, "$lte": date_to_iso.year}},
                               {"month": {"$gte": date_from_iso.month,"$lte": date_to_iso.month}},
                               {"day": {"$gte": date_from_iso.day, "$lte": date_to_iso.day}},
                               {"hour": {"$gte": date_from_iso.hour, "$lte": date_to_iso.hour}},
                               {"minuts": {"$gte": date_from_iso.minute, "$lte": date_to_iso.minute}}],
                      }
                     },
                     {
                          "$sort": {field_to_sort:-1}
                     },
                     {"$limit" :  limit}]

                # aggregation query (application):
                # Match the range of date from - to:
                # Then:
                # Group for Date and Key :
                # - compute the total response time for Key
                # - compute the total request for Key
                # - compute the total error for Key
                aggregation_for_date_and_key = [
                    {
                        "$set":
                        {
                            "_id": 0,
                            "year": {"$year": "$Creation_datetime"},
                            "month": {"$month": "$Creation_datetime"},
                            "day": {"$dayOfMonth": "$Creation_datetime"},
                            "hour": {"$hour": "$Creation_datetime"},
                            "minuts": {"$minute": "$Creation_datetime"}
                        },

                    },
                    {
                        "$set": {
                            "dateNotSeconds": {"$concat": [{"$toString": "$year"}, "-", {"$toString": "$month"}, "-", {"$toString": "$day"}, " ", {"$toString": "$hour"}, ":", {"$toString": "$minuts"}, ":00"]}
                        }
                    },
                    {"$match":
                     {"$and": [{"year": {"$gte": date_from_iso.year, "$lte": date_to_iso.year}},
                               {"month": {"$gte": date_from_iso.month,"$lte": date_to_iso.month}},
                               {"day": {"$gte": date_from_iso.day, "$lte": date_to_iso.day}},
                               {"hour": {"$gte": date_from_iso.hour, "$lte": date_to_iso.hour}},
                               {"minuts": {"$gte": date_from_iso.minute, "$lte": date_to_iso.minute}}],
                      }
                     },
                    {
                        "$group":
                        {"_id": {"date": "$dateNotSeconds", "key": "$Key"},
                         "total_response_time_ms": {"$sum": "$Response_time"},
                         "total_requests": {"$sum": 1},
                         "total_errors": {"$sum": {"$cond": [
                             {"$eq": ["$Response_code", 500]},
                             1,
                             0
                         ]}}
                         }

                    }
                ]

                # the result of aggregation
                result_values = aggregation_collection(
                    collection_name, aggregation_for_date_and_key)

                # result of aggregation for logs (last 10 logs and desc for creation_date)
                result_logs = aggregation_collection(
                    collection_name, last_10_logs_query)

                # create object to return api
                objectRetrieve = OutputRetrive()

                # create list of values
                list_values = []

                # create list of logs
                list_logs = []

                # elaborate the values from aggregation result
                if result_values:
                    for i in result_values:
                        value = OutputValue()
                        # the key aggregate
                        value.key = i['_id']['key']
                        value.total_response_time_ms = i['total_response_time_ms']
                        value.total_requests = i['total_requests']
                        value.total_errors = i['total_errors']
                        # the date aggregate
                        value.creation_datetime = i['_id']['date']
                        list_values.append(value)

                # elaborate the values from query for logs result
                for i in result_logs:
                    log = OutputLogs()
                    log.key = i['Key']
                    log.payload = i['Payload']
                    log.creation_datetime = i['Creation_datetime']
                    log.response_time = i['Response_time']
                    log.response_code = i['Response_code']
                    list_logs.append(log)

                # set the values returned
                objectRetrieve.values = list_values

                # set the logs returned
                objectRetrieve.logs = list_logs

                # return the entire object (results)
                return objectRetrieve

        else:
            # otherwise not Authorized
            output.status_code = 401
            output.message = 'Not Authorized'
            return output
    except TooManyRedirects:
        raise HTTPException(status_code=404,
                            detail="Many Redirects")
    except HTTPError:
        raise HTTPException(status_code=500,
                            detail="Server Error 500")
