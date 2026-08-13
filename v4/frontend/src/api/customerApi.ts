import type { Customer, LoginCredentials, RegisterCustomerPayload } from "../types/customer";
import { apiRequest } from "./client";
import type { ResponseEntity } from "../types/api";

export async function loginCustomer(credentials: LoginCredentials): Promise<Customer> {
    const response = await apiRequest<ResponseEntity<Customer>>('/customers/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
    });

    return response.data!;
}


export async function getAllCustomers(): Promise<Customer | null> {
    const response = await apiRequest<ResponseEntity<Customer>>(`/`);

    return response.data;
}