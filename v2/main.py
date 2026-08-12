from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from routers.CustomerRouter import router as crouter
from routers.AccountRouter import router as arouter
from routers.TransactionRouter import router as trouter

app = FastAPI()

app.include_router(crouter, prefix="/api/v1/customers")
app.include_router(arouter, prefix="/api/v1/accounts")
app.include_router(trouter, prefix="api/v1/transactions")


# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED