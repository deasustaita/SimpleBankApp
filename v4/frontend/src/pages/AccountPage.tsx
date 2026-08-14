import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import type { Account } from "../types/account";
import type { Transaction } from "../types/transaction";
import { fetchAccountById } from "../api/accountApi";
import { fetchTransactionsByAccount } from "../api/transactionApi";
import { TransactionTable } from "../components/transaction/TransactionTable";

export function AccountPage() {
    const { accountId } = useParams();
    const navigate = useNavigate();

    const [account, setAccount] = useState<Account | null>(null);
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadData() {
            if (!accountId) {
                return;
            }

            try {
                const [accountData, transactionData] = await Promise.all([
                    fetchAccountById(accountId),
                    fetchTransactionsByAccount(accountId),
                ]);

                setAccount(accountData);
                setTransactions(transactionData);
            } catch (error) {
                console.error('Error loading account:', error);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, [accountId]);

    if (loading) return <p>Loading account...</p>;
    if (!account) return <p>Account not found.</p>;

    const formattedBalance = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(Number(account.balance) || 0);

    return (
        <div>
            <button onClick={() => navigate('/dashboard')}>Back to Dashboard</button>

            <h1>{account.acc_type.toUpperCase()}</h1>
            <p><strong>Balance</strong></p>
            <p>{formattedBalance}</p>

            <button onClick={() => navigate(`/accounts/${accountId}/transaction`)}>
                Make Transaction
            </button>

            <h2>Transactions</h2>
            <TransactionTable transactions={transactions} />
        </div>
    );
}
