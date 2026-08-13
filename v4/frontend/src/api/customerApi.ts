import type { Customer } from "../types/customer";
import { apiRequest } from "./client";

export async function getAllCustomers(): Promise<Customer> {
    return apiRequest<Customer>(`/`);
}