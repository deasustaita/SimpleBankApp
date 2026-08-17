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
    const [deleting, setDeleting] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deleteConfirmationText, setDeleteConfirmationText] = useState("");
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

        if (deleteConfirmationText.trim() !== "CLOSE") {
            setError("Account close cancelled. Confirmation text did not match.");
            return;
        }

        setDeleting(true);

        try {
            await deleteAccount(accountId);
            setShowDeleteModal(false);
            navigate("/accounts");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to close account.");
        } finally {
            setDeleting(false);
        }
    }

    function openDeleteModal() {
        setDeleteConfirmationText("");
        setError("");
        setShowDeleteModal(true);
    }

    function closeDeleteModal() {
        if (deleting) {
            return;
        }

        setShowDeleteModal(false);
        setDeleteConfirmationText("");
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
                <button className="btn btn-danger" onClick={openDeleteModal}>
                    Close Account
                </button>
            </div>

            {showDeleteModal && (
                <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="close-account-title">
                    <div className="modal-card">
                        <h2 id="close-account-title">Close Account</h2>
                        <p>
                            This will permanently close this account. Type <strong>CLOSE</strong> to confirm.
                        </p>
                        <input
                            type="text"
                            className="auth-input"
                            value={deleteConfirmationText}
                            onChange={(event) => setDeleteConfirmationText(event.target.value)}
                            placeholder="Type CLOSE"
                        />
                        <div className="modal-actions">
                            <button type="button" className="btn btn-secondary" onClick={closeDeleteModal} disabled={deleting}>
                                Cancel
                            </button>
                            <button type="button" className="btn" onClick={handleDelete} disabled={deleting}>
                                {deleting ? "Closing..." : "Confirm Close"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
