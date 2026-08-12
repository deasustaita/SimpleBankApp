from dotenv import dotenv_values
from pymongo import MongoClient

from fastapi import FastAPI
from routers import CustomerRouter

config = dotenv_values(".env")
app = FastAPI()

app.include_router(CustomerRouter.router, prefix="/api/v1/customers")


# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED