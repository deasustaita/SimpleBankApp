import type { Account } from "../types/account";

const BASE_URL = "http://localhost:8000/api/v1"

export async function fetchAccountsByCustomer(customerId: string): Promise<Account[]> {
    const response = await fetch(`${BASE_URL}/${customerId}/accounts`);

    if (!response.ok) {
        throw new Error('Failed to fetch accounts.');
    }

    const result = await response.json();
    return result.data;
}