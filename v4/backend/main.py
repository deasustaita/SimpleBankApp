from dotenv import dotenv_values
from pymongo import MongoClient

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import CustomerRouter, AccountRouter, TransactionRouter

config = dotenv_values(".env")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_start():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown():
    app.mongodb_client.close()


app.include_router(CustomerRouter.router, prefix="/api/v1/customers")
app.include_router(AccountRouter.router, prefix="/api/v1")
app.include_router(TransactionRouter.router, prefix="/api/v1/{customer_id}/transactions")

# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED