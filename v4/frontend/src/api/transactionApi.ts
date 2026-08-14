import type { Transaction } from "../types/transaction";
import { apiRequest } from "./client";
import type { ResponseEntity } from "../types/api";

export async function fetchTransactionsByAccount(accountId: string): Promise<Transaction[]> {
    const response = await apiRequest<ResponseEntity<Transaction[]>>(`/transactions/account/${accountId}`);

    return response.data ?? [];
}

export async function fetchTransactionsByCustomer(customerId: string): Promise<Transaction[]> {
    const response = await apiRequest<ResponseEntity<Transaction[]>>(`/transactions/customer/${customerId}`);

    return response.data ?? [];
}

export async function depositMoney(accountId: string, amount: number): Promise<Transaction> {
    const response = await apiRequest<ResponseEntity<Transaction>>(`/transactions/deposit?account_id=${accountId}`, {
        method: 'POST',
        body: JSON.stringify({ txn_type: 'DEPOSIT', amount }),
    });

    return response.data!;
}

export async function withdrawMoney(accountId: string, amount: number): Promise<Transaction> {
    const response = await apiRequest<ResponseEntity<Transaction>>(`/transactions/withdrawal?account_id=${accountId}`, {
        method: 'POST',
        body: JSON.stringify({ txn_type: 'WITHDRAWAL', amount }),
    });

    return response.data!;
}

export async function transferMoney(accountId: string, destAccountId: string, amount: number): Promise<Transaction> {
    const response = await apiRequest<ResponseEntity<Transaction>>(`/transactions/transfer?account_id=${accountId}`, {
        method: 'POST',
        body: JSON.stringify({ txn_type: 'TRANSFER', amount, dest_account_id: destAccountId }),
    });

    return response.data!;
}
