import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { depositMoney, withdrawMoney, transferMoney } from "../api/transactionApi";

type TxnType = "DEPOSIT" | "WITHDRAWAL" | "TRANSFER";

export function CreateTransactionPage() {
    const { accountId } = useParams();
    const navigate = useNavigate();

    const [txnType, setTxnType] = useState<TxnType>("DEPOSIT");
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
        <div>
            <h1>Make a Transaction</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        <input
                            type="radio"
                            name="txnType"
                            value="DEPOSIT"
                            checked={txnType === "DEPOSIT"}
                            onChange={() => setTxnType("DEPOSIT")}
                        />
                        Deposit
                    </label>

                    <label>
                        <input
                            type="radio"
                            name="txnType"
                            value="WITHDRAWAL"
                            checked={txnType === "WITHDRAWAL"}
                            onChange={() => setTxnType("WITHDRAWAL")}
                        />
                        Withdrawal
                    </label>

                    <label>
                        <input
                            type="radio"
                            name="txnType"
                            value="TRANSFER"
                            checked={txnType === "TRANSFER"}
                            onChange={() => setTxnType("TRANSFER")}
                        />
                        Transfer
                    </label>
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

                {error && <p>{error}</p>}

                <button type="submit" disabled={loading}>
                    {loading ? "Submitting..." : "Submit"}
                </button>
            </form>

            <button onClick={() => navigate(`/accounts/${accountId}`)}>Cancel</button>
        </div>
    );
}
