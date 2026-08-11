from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    username: str

    ## For use in later developments but for the moment only the above is needed.
    # name: str
    # password: str
    # accounts: Accounts[]


