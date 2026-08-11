from models.Customer import Customer
from models.Account import Account
from datetime import datetime

customers = [
    Customer(id=1, 
             username="dsustaita",
             password="password",
             name="Dea Sustaita",
             email="deasustaita@gmail.com",
             accounts=[],
             time_created=datetime.now().isoformat()),
    Customer(id=2, 
             username="ifiorentino",
             password="password",
             name="Isabel Fiorentino",
             email="ifiorentino@gmail.com",
             accounts=[],
             time_created=datetime.now().isoformat())
]