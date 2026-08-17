import type { Transaction } from "../../types/transaction";

interface TransactionTableProps {
    transactions: Transaction[];
}

const currencyFormatter = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

export function TransactionTable({ transactions }: TransactionTableProps) {
    if (transactions.length === 0) {
        return <p>No transactions yet.</p>;
    }

    return (
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Amount</th>
                </tr>
            </thead>

            <tbody>
                {transactions.map((transaction) => (
                    <tr key={transaction.txn_id}>
                        <td>{new Date(transaction.created_at).toLocaleDateString()}</td>
                        <td>{transaction.txn_type}</td>
                        <td>${currencyFormatter.format(transaction.amount)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
