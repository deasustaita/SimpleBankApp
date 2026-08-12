from dotenv import dotenv_values
from pymongo import MongoClient

from fastapi import FastAPI
from routers import CustomerRouter, AccountRouter

config = dotenv_values(".env")
app = FastAPI()


@app.on_event("startup")
def on_start():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown():
    app.mongodb_client.close()


app.include_router(CustomerRouter.router, prefix="/api/v1/customers")
app.include_router(AccountRouter.router, prefix="/api/v1")

# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED