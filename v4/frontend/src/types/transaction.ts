export interface Transaction {
    txn_id: string;
    account_id: string;
    amount: number;
    created_at: string;
    txn_type: 'DEPOSIT' | 'WITHDRAWAL' | 'TRANSFER';
    dest_account_id?: string;
}
