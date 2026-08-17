from models.Customer import Customer

from typing import List, Optional
from bson import ObjectId


# manipulation of data occurs here
class CustomerRepository:
    def __init__(self, database):
        self._data = database["Customer"]

    def find_customers(self) -> List[Customer]:
        # return the data of all customers in the database
        customers = self._data.find()
        return [Customer(**doc) for doc in customers]

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        if not ObjectId.is_valid(customer_id):
            return None

        customer = self._data.find_one({"_id": ObjectId(customer_id)})

        if customer:
            return Customer(**customer)

        return None

    def find_by_username(self, username: str) -> Optional[Customer]:
        customer = self._data.find_one({"username": username})
        if customer:
            return Customer(**customer)
        return None

    def make_customer(self, customer: Customer) -> Customer:
        customer_data = customer.model_dump(by_alias=True, exclude_none=True)

        result = self._data.insert_one(customer_data)

        customer.id = str(result.inserted_id)

        return customer

    def update_customer(self, customer_id: str, up_customer: Customer) -> Optional[Customer]:
        if not ObjectId.is_valid(customer_id):
            return None

        up_customer.id = customer_id

        customer_data = up_customer.model_dump(
            by_alias=True,
            exclude_none=True
        )

        customer_data.pop("_id", None)

        result = self._data.update_one(
            {"_id": ObjectId(customer_id)},
            {"$set": customer_data}
        )

        if result.matched_count == 0:
            return None

        return up_customer

    def update_customer_fields(self, customer_id: str, fields: dict) -> Optional[Customer]:
        if not ObjectId.is_valid(customer_id):
            return None

        sanitized = {key: value for key, value in fields.items() if value is not None and key != "_id"}

        if not sanitized:
            return self.find_by_id(customer_id)

        result = self._data.update_one(
            {"_id": ObjectId(customer_id)},
            {"$set": sanitized}
        )

        if result.matched_count == 0:
            return None

        return self.find_by_id(customer_id)

    def remove_customer(self, customer_id: str):
        if not ObjectId.is_valid(customer_id):
            return False

        result = self._data.delete_one(
            {"_id": ObjectId(customer_id)}
        )

        return result.deleted_count > 0


## wrap in a ResponseEntity rather than return a list
# 1 example of getall getbyid post put delete rest method call(controller -> service -> repo)