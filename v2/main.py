from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from routers.CustomerRouter import router
app = FastAPI()

app.include_router(router, prefix="/api/v1/customers")

# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED