import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import type { Account } from "../types/account";
import { fetchAccountById, updateAccount, deleteAccount } from "../api/accountApi";

export function AccountSettingsPage() {
    const { accountId } = useParams();
    const navigate = useNavigate();

    const [account, setAccount] = useState<Account | null>(null);
    const [nickname, setNickname] = useState("");
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadAccount() {
            if (!accountId) return;
            try {
                const data = await fetchAccountById(accountId);
                setAccount(data);
                setNickname(data.nickname ?? "");
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unable to load account.");
            } finally {
                setLoading(false);
            }
        }
        loadAccount();
    }, [accountId]);

    async function handleSave(event: React.FormEvent) {
        event.preventDefault();
        if (!accountId) return;

        setError("");
        setSaving(true);
        try {
            const updated = await updateAccount(accountId, { nickname });
            setAccount(updated);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to save settings.");
        } finally {
            setSaving(false);
        }
    }

    async function handleToggleFavorite() {
        if (!accountId || !account) return;
        try {
            const updated = await updateAccount(accountId, { is_favorite: !account.is_favorite });
            setAccount(updated);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to update favorite status.");
        }
    }

    async function handleDelete() {
        if (!accountId) return;
        if (!window.confirm("Are you sure you want to close this account? This cannot be undone.")) {
            return;
        }
        try {
            await deleteAccount(accountId);
            navigate("/accounts");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to close account.");
        }
    }

    if (loading) return <p className="page">Loading account settings...</p>;
    if (!account) return <p className="page">Account not found.</p>;

    return (
        <div className="page">
            <button className="btn btn-secondary" onClick={() => navigate(`/accounts/${accountId}`)}>
                Back to Account
            </button>

            <h1>Account Settings</h1>

            <div className="panel">
                <p><strong>Account Type:</strong> {account.acc_type}</p>
                {account.acc_type === "CHECKING" && (
                    <p><strong>Overdraft Limit:</strong> ${account.overdraft_limit ?? 0}</p>
                )}
                <p>
                    <strong>Favorite:</strong>{" "}
                    <button className="favorite-star active" onClick={handleToggleFavorite} style={{ verticalAlign: "middle" }}>
                        {account.is_favorite ? "★ Favorited" : "☆ Add to favorites"}
                    </button>
                </p>
            </div>

            <form onSubmit={handleSave}>
                <div>
                    <label htmlFor="nickname">Nickname</label>
                    <input
                        id="nickname"
                        type="text"
                        value={nickname}
                        onChange={(event) => setNickname(event.target.value)}
                        placeholder="e.g. Rainy Day Fund"
                    />
                </div>

                {error && <p className="error-text">{error}</p>}

                <button className="btn" type="submit" disabled={saving}>
                    {saving ? "Saving..." : "Save Changes"}
                </button>
            </form>

            <div style={{ marginTop: 32 }}>
                <button className="btn btn-danger" onClick={handleDelete}>
                    Close Account
                </button>
            </div>
        </div>
    );
}
