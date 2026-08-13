import type { Account } from "../types/account";
import { apiRequest } from "./client";
import type { ResponseEntity } from "../types/responseEntity";

export async function fetchAccountsByCustomer(customerId: string): Promise<Account[]> {
    const response = await apiRequest<ResponseEntity<Account[]>>(`/${customerId}/accounts`);

    return response.data ?? [];
}