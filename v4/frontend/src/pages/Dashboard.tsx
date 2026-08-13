import { useState, useEffect } from "react";
import type { Account } from "../types/account";
import { fetchAccountsByCustomer } from "../api/accountApi";
import { AccountCard } from "../components/account/AccountCard";

export function DashboardPage() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadData() {
            try {
                const data = await fetchAccountsByCustomer('6a7ca44d1ef36438893a95e9')
                setAccounts(data);
            } catch (error) {
                console.error('Error loading dashboard:', error);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, []);

    if (loading) return <p>Loading your accounts...</p>;
    return (
        <div>
            <h2>Customer Dashboard</h2>
            <div>
                {accounts.map((account, index) => (
                    <AccountCard 
                        key={account.account_id || index} 
                        account={account} 
                    />
                ))}
            </div>
        </div>
    )
}