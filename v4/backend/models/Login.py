from pydantic import BaseModel

class LoginCredentialsRequest(BaseModel):
    username: str
    password: str