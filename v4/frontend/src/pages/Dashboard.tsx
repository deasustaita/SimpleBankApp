import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import type { Account } from "../types/account";
import { fetchAccountsByCustomer } from "../api/accountApi";
import { AccountCard } from "../components/account/AccountCard";
import { useAuth } from "../context/AuthContext";

export function DashboardPage() {
    const { customer, logout } = useAuth();
    const navigate = useNavigate();

    const [accounts, setAccounts] = useState<Account[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadData() {
            if (!customer) {
                return;
            }

            try {
                const data = await fetchAccountsByCustomer(customer._id)
                setAccounts(data);
            } catch (error) {
                console.error('Error loading dashboard:', error);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, [customer]);

    function handleLogout() {
        logout();
        navigate("/login");
    }

    if (loading) return <p>Loading your accounts...</p>;
    return (
        <div>
            <header>
                <h1>SimpleBank</h1>
                <button onClick={handleLogout}>Logout</button>
            </header>

            <main>
                <h2>Welcome, {customer!.name}</h2>
                <p>User ID: {customer!._id} </p>
                <p>Username: {customer!.username}</p>
                <p>Email: {customer!.email}</p>

                <h2>Your Accounts</h2>
                <button onClick={() => navigate('/accounts/create')}> Create Account</button>
                {accounts.length === 0 ? (
                    <p>You don't have any accounts yet.</p>
                ): (
                    <div>
                        {accounts.map((account, index) => (
                            <AccountCard 
                                key={account.account_id || index}
                                account={account}
                            />
                        ))}
                    </div>
                )}
            </main>

        </div>
    )
}