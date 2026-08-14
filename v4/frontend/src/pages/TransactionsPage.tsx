import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import type { Account } from "../types/account";
import type { Transaction } from "../types/transaction";
import { fetchAccountsByCustomer } from "../api/accountApi";
import { fetchTransactionsByCustomer } from "../api/transactionApi";
import { TransactionTable } from "../components/transaction/TransactionTable";
import { useAuth } from "../context/AuthContext";

const TXN_TYPES = [
    { value: "DEPOSIT", label: "Deposit" },
    { value: "WITHDRAWAL", label: "Withdrawal" },
    { value: "TRANSFER", label: "Transfer" },
] as const;

export function TransactionsPage() {
    const { customer } = useAuth();
    const navigate = useNavigate();

    const [accounts, setAccounts] = useState<Account[]>([]);
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [selectedAccountId, setSelectedAccountId] = useState("");
    const [loading, setLoading] = useState(true);
    const [showNewTransaction, setShowNewTransaction] = useState(false);

    useEffect(() => {
        async function loadData() {
            if (!customer) return;
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
                if (accountData.length > 0) {
                    setSelectedAccountId(accountData[0].account_id);
                }
            } catch (error) {
                console.error('Error loading transactions:', error);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, [customer]);

    function handleStartTransaction(type: string) {
        if (!selectedAccountId) return;
        navigate(`/accounts/${selectedAccountId}/transaction?type=${type}`);
    }

    if (loading) return <p className="page">Loading transactions...</p>;

    return (
        <div className="page">
            <div className="panel-header">
                <h1>All Transactions</h1>
                <button className="btn" onClick={() => setShowNewTransaction((prev) => !prev)}>
                    {showNewTransaction ? "Cancel" : "New Transaction"}
                </button>
            </div>

            {showNewTransaction && (
                <div className="panel">
                    <label htmlFor="accountSelect">Account</label>
                    <select
                        id="accountSelect"
                        value={selectedAccountId}
                        onChange={(event) => setSelectedAccountId(event.target.value)}
                    >
                        {accounts.map((account) => (
                            <option key={account.account_id} value={account.account_id}>
                                {account.nickname || account.acc_type} · {account.account_id}
                            </option>
                        ))}
                    </select>

                    <div className="txn-type-group" style={{ marginTop: 12 }}>
                        {TXN_TYPES.map((type) => (
                            <button
                                key={type.value}
                                className="txn-type-btn"
                                onClick={() => handleStartTransaction(type.value)}
                            >
                                {type.label}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <TransactionTable transactions={transactions} />
        </div>
    );
}
