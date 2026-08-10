from models import Customer

# manipulation of data occurs here
class CustomerRepository:

    def get_all_customers():
        pass # return the data of all customers in the database

    def get_customer_by_id():
        pass # find specific customer by their id

## wrap in a ResponseEntity rather than return a list
# 1 example of getall getbyid post put delete rest method call(controller -> service -> repo)