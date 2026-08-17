import { useNavigate } from "react-router-dom";
import type { Account } from "../../types/account";
import { updateAccount } from "../../api/accountApi";


interface AccountCardProps {
    account: Account;
    onFavoriteChange?: (account: Account) => void;
}

export function AccountCard({ account, onFavoriteChange }: AccountCardProps) {
    const navigate = useNavigate();

    const formattedBalance = new Intl.NumberFormat('en-US', {
        style:'currency',
        currency:'USD'
    }).format(Number(account?.balance) || 0)

    async function handleToggleFavorite(event: React.MouseEvent) {
        event.stopPropagation();
        try {
            const updated = await updateAccount(account.account_id, { is_favorite: !account.is_favorite });
            onFavoriteChange?.(updated);
        } catch (error) {
            console.error('Failed to update favorite status:', error);
        }
    }

    return (
        <div
            className="card"
            onClick={() => navigate(`/accounts/${account.account_id}`)}
            style={{ cursor: 'pointer' }}
        >
            <div className="panel-header">
                <h3>{account.nickname || account.acc_type.toUpperCase()}</h3>
                <button
                    className={`favorite-star${account.is_favorite ? ' active' : ''}`}
                    onClick={handleToggleFavorite}
                    title={account.is_favorite ? 'Remove from favorites' : 'Add to favorites'}
                >
                    {account.is_favorite ? '★' : '☆'}
                </button>
            </div>
            <p>{account.acc_type.toUpperCase()} · Account ID: {account.account_id}</p>
            <p><strong>Balance: </strong><span>{formattedBalance}</span></p>
        </div>
    )
}