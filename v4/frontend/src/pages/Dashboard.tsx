import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import type { Account } from "../types/account";
import type { Transaction } from "../types/transaction";
import { fetchAccountsByCustomer } from "../api/accountApi";
import { fetchTransactionsByCustomer } from "../api/transactionApi";
import { AccountCard } from "../components/account/AccountCard";
import { TransactionTable } from "../components/transaction/TransactionTable";
import { useAuth } from "../context/AuthContext";

const RECENT_TRANSACTION_LIMIT = 5;

export function DashboardPage() {
    const { customer } = useAuth();
    const navigate = useNavigate();

    const [accounts, setAccounts] = useState<Account[]>([]);
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadData() {
            if (!customer) {
                return;
            }

            try {
                const [accountData, transactionData] = await Promise.all([
                    fetchAccountsByCustomer(customer._id),
                    fetchTransactionsByCustomer(customer._id),
                ]);

                setAccounts(accountData);
                setTransactions(
                    [...transactionData].sort(
                        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
                    )
                );
            } catch (error) {
                console.error('Error loading dashboard:', error);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, [customer]);

    function handleFavoriteChange(updated: Account) {
        setAccounts((prev) =>
            prev.map((account) => (account.account_id === updated.account_id ? updated : account))
        );
    }

    if (loading) return <p className="page">Loading your accounts...</p>;

    const favoriteAccounts = accounts.filter((account) => account.is_favorite);
    const recentTransactions = transactions.slice(0, RECENT_TRANSACTION_LIMIT);

    return (
        <div className="page">
            <h2>Welcome, {customer!.name}</h2>
            <p>Username: {customer!.username}</p>
            <p>Email: {customer!.email}</p>

            <div className="panel">
                <div className="panel-header">
                    <h2>Favorite Accounts</h2>
                    <div className="btn-group">
                        <button className="btn btn-secondary" onClick={() => navigate('/accounts')}>
                            See All
                        </button>
                        <button className="btn" onClick={() => navigate('/accounts/create')}>
                            Make Account
                        </button>
                    </div>
                </div>

                {favoriteAccounts.length === 0 ? (
                    <p>Star an account to pin it here.</p>
                ) : (
                    <div className="grid">
                        {favoriteAccounts.map((account, index) => (
                            <AccountCard
                                key={account.account_id || index}
                                account={account}
                                onFavoriteChange={handleFavoriteChange}
                            />
                        ))}
                    </div>
                )}
            </div>

            <div className="panel">
                <div className="panel-header">
                    <h2>Recent Transactions</h2>
                    <button className="btn btn-secondary" onClick={() => navigate('/transactions')}>
                        See All
                    </button>
                </div>
                <TransactionTable transactions={recentTransactions} />
            </div>
        </div>
    )
}