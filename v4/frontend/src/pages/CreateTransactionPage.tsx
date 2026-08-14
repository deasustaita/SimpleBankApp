import { useState } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { depositMoney, withdrawMoney, transferMoney } from "../api/transactionApi";

type TxnType = "DEPOSIT" | "WITHDRAWAL" | "TRANSFER";

const TXN_TYPES: { value: TxnType; label: string }[] = [
    { value: "DEPOSIT", label: "Deposit" },
    { value: "WITHDRAWAL", label: "Withdrawal" },
    { value: "TRANSFER", label: "Transfer" },
];

export function CreateTransactionPage() {
    const { accountId } = useParams();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const initialType = (searchParams.get("type") as TxnType) || "DEPOSIT";

    const [txnType, setTxnType] = useState<TxnType>(initialType);
    const [amount, setAmount] = useState("");
    const [destAccountId, setDestAccountId] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event: React.FormEvent) {
        event.preventDefault();

        if (!accountId) {
            return;
        }

        setError("");
        setLoading(true);

        try {
            const numericAmount = Number(amount);

            if (txnType === "DEPOSIT") {
                await depositMoney(accountId, numericAmount);
            } else if (txnType === "WITHDRAWAL") {
                await withdrawMoney(accountId, numericAmount);
            } else {
                await transferMoney(accountId, destAccountId, numericAmount);
            }

            navigate(`/accounts/${accountId}`);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to complete transaction.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="page">
            <h1>Make a Transaction</h1>

            <form onSubmit={handleSubmit}>
                <div className="txn-type-group">
                    {TXN_TYPES.map((type) => (
                        <button
                            key={type.value}
                            type="button"
                            className={`txn-type-btn${txnType === type.value ? ' active' : ''}`}
                            onClick={() => setTxnType(type.value)}
                        >
                            {type.label}
                        </button>
                    ))}
                </div>

                {txnType === "TRANSFER" && (
                    <div>
                        <label htmlFor="destAccountId">Destination Account ID</label>
                        <input
                            id="destAccountId"
                            type="text"
                            value={destAccountId}
                            onChange={(event) => setDestAccountId(event.target.value)}
                            required
                        />
                    </div>
                )}

                <div>
                    <label htmlFor="amount">Amount</label>
                    <input
                        id="amount"
                        type="number"
                        min="0.01"
                        step="0.01"
                        value={amount}
                        onChange={(event) => setAmount(event.target.value)}
                        required
                    />
                </div>

                {error && <p className="error-text">{error}</p>}

                <button className="btn" type="submit" disabled={loading}>
                    {loading ? "Submitting..." : "Submit"}
                </button>
            </form>

            <button className="btn btn-secondary" onClick={() => navigate(`/accounts/${accountId}`)}>Cancel</button>
        </div>
    );
}
