export interface Account {
    account_id: string;
    customer_id: string;
    acc_type: 'checking' | 'savings';
    balance: number;
}