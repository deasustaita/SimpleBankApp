import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import type { Account } from "../types/account";
import { fetchAccountsByCustomer } from "../api/accountApi";
import { AccountCard } from "../components/account/AccountCard";
import { useAuth } from "../context/AuthContext";

export function AccountsPage() {
    const { customer } = useAuth();
    const navigate = useNavigate();

    const [accounts, setAccounts] = useState<Account[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadAccounts() {
            if (!customer) {
                return;
            }
            try {
                const data = await fetchAccountsByCustomer(customer._id);
                setAccounts(data);
            } catch (error) {
                console.error('Error loading accounts:', error);
            } finally {
                setLoading(false);
            }
        }
        loadAccounts();
    }, [customer]);

    function handleFavoriteChange(updated: Account) {
        setAccounts((prev) =>
            prev.map((account) => (account.account_id === updated.account_id ? updated : account))
        );
    }

    if (loading) return <p className="page">Loading accounts...</p>;

    return (
        <div className="page">
            <div className="panel-header">
                <h1>All Accounts</h1>
                <button className="btn" onClick={() => navigate('/accounts/create')}>
                    Make Account
                </button>
            </div>

            {accounts.length === 0 ? (
                <p>You don't have any accounts yet.</p>
            ) : (
                <div className="grid">
                    {accounts.map((account, index) => (
                        <AccountCard
                            key={account.account_id || index}
                            account={account}
                            onFavoriteChange={handleFavoriteChange}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}
