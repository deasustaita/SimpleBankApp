import type { Account } from "../types/account";
import { apiRequest } from "./client";
import type { ResponseEntity } from "../types/api";

export async function fetchAccountsByCustomer(customerId: string): Promise<Account[]> {
    const response = await apiRequest<ResponseEntity<Account[]>>(`/${customerId}/accounts`);

    return response.data ?? [];
}

export async function fetchAccountById(accountId: string): Promise<Account> {
    const response = await apiRequest<ResponseEntity<Account>>(`/accounts/${accountId}`);

    return response.data!;
}

export async function createAccount(customerId: string, accountType: string, balance?: number): Promise<Account> {
    const response = await apiRequest<ResponseEntity<Account>>(`/${customerId}/accounts`, {
        method: 'POST',
        body: JSON.stringify({acc_type: accountType, balance : balance ?? 0}),
    });

    return response.data!;
}