export interface Account {
    account_id: string;
    customer_id: string;
    acc_type: 'CHECKING' | 'SAVINGS';
    balance: number;
    nickname?: string | null;
    is_favorite: boolean;
    overdraft_limit?: number;
}

export interface AccountUpdatePayload {
    nickname?: string;
    is_favorite?: boolean;
}