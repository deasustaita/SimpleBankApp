from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from routers.CustomerRouter import router as crouter
from routers.AccountRouter import router as arouter


app = FastAPI()

app.include_router(crouter, prefix="/api/v1/customers")
app.include_router(arouter, prefix="/api/v1/accounts")

# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED