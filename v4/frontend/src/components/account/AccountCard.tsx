import type { Account } from "../../types/account";


interface AccountCardProps {
    account: Account;
}

export function AccountCard({ account }: AccountCardProps) {
    const formattedBalance = new Intl.NumberFormat('en-US', {
        style:'currency',
        currency:'USD'
    }).format(Number(account?.balance) || 0)

    return (
        <div>
            <h3>{account.acc_type.toUpperCase()}</h3>
            <p>Account ID: {account.account_id}</p>
            <p><strong>Balance: </strong><span>{formattedBalance}</span></p>
        </div>
    )
}