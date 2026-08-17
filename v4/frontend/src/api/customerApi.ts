import type { Customer, CustomerUpdatePayload, LoginCredentials, RegisterCustomerPayload } from "../types/customer";
import { apiRequest } from "./client";
import type { ResponseEntity } from "../types/api";

interface LoginTokenData {
    access_token: string;
    token_type: string;
}

export async function loginCustomer(credentials: LoginCredentials): Promise<Customer> {
    const response = await apiRequest<ResponseEntity<LoginTokenData>>('/customers/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
    });

    const token = response.data?.access_token;

    if (!token) {
        throw new Error('Login succeeded but no access token was returned.');
    }

    localStorage.setItem('sb_access_token', token);

    return getCurrentCustomer();
}

export async function getCurrentCustomer(): Promise<Customer> {
    const response = await apiRequest<ResponseEntity<Customer>>('/customers/me');

    if (!response.data) {
        throw new Error('Unable to load current customer profile.');
    }

    return response.data;
}


export async function getAllCustomers(): Promise<Customer[] | null> {
    const response = await apiRequest<ResponseEntity<Customer[]>>('/customers/');

    return response.data;
}

export async function registerCustomer(payload:RegisterCustomerPayload): Promise<Customer> {
    const response = await apiRequest<ResponseEntity<Customer>>('/customers/',{
        method: 'POST',
        body: JSON.stringify(payload),
    });

    return response.data!;
}

export async function updateCurrentCustomer(payload: CustomerUpdatePayload): Promise<Customer> {
    const response = await apiRequest<ResponseEntity<Customer>>('/customers/me', {
        method: 'PATCH',
        body: JSON.stringify(payload),
    });

    if (!response.data) {
        throw new Error('Unable to update customer profile.');
    }

    return response.data;
}

export async function deleteCurrentCustomer(): Promise<void> {
    await apiRequest<ResponseEntity<null>>('/customers/me', {
        method: 'DELETE',
    });
}