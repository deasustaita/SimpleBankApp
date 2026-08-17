import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function CustomerSettingsPage() {
  const navigate = useNavigate();
  const { customer, updateProfile, deleteMyAccount } = useAuth();
  const currentCustomer = customer;

  const [name, setName] = useState(customer?.name ?? '');
  const [email, setEmail] = useState(customer?.email ?? '');
  const [username, setUsername] = useState(customer?.username ?? '');
  const [password, setPassword] = useState('');
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteConfirmationText, setDeleteConfirmationText] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  if (!currentCustomer) {
    return <p className="page">No customer session found.</p>;
  }

  async function handleDeleteAccount() {
    if (deleteConfirmationText.trim() !== 'DELETE') {
      setError('Account deletion cancelled. Confirmation text did not match.');
      return;
    }

    setError('');
    setSuccess('');
    setDeleting(true);

    try {
      await deleteMyAccount();
      setShowDeleteModal(false);
      navigate('/', { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to delete account.');
    } finally {
      setDeleting(false);
    }
  }

  function openDeleteModal() {
    setError('');
    setSuccess('');
    setDeleteConfirmationText('');
    setShowDeleteModal(true);
  }

  function closeDeleteModal() {
    if (deleting) {
      return;
    }

    setShowDeleteModal(false);
    setDeleteConfirmationText('');
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    if (!currentCustomer) {
      return;
    }

    setError('');
    setSuccess('');

    const payload: {
      name?: string;
      email?: string;
      username?: string;
      password?: string;
    } = {};

    if (name.trim() !== currentCustomer.name) payload.name = name.trim();
    if (email.trim() !== currentCustomer.email) payload.email = email.trim();
    if (username.trim() !== currentCustomer.username) payload.username = username.trim();
    if (password.trim().length > 0) payload.password = password;

    if (Object.keys(payload).length === 0) {
      setSuccess('No changes to save.');
      return;
    }

    setSaving(true);
    try {
      await updateProfile(payload);
      setPassword('');
      setSuccess('Profile updated successfully.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to update profile.');
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="page">
      <div className="panel profile-settings-panel">
        <div className="panel-header">
          <h1>Customer Settings</h1>
          <button className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
            Back to Dashboard
          </button>
        </div>

        <p className="profile-id-text">
          <strong>Customer ID:</strong> {currentCustomer._id}
        </p>

        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="customer-name">Name</label>
            <input
              id="customer-name"
              type="text"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="customer-email">Email</label>
            <input
              id="customer-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="customer-username">Username</label>
            <input
              id="customer-username"
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="customer-password">New Password (optional)</label>
            <input
              id="customer-password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Leave blank to keep current password"
            />
          </div>

          {error && <p className="error-text">{error}</p>}
          {success && <p className="success-text">{success}</p>}

          <button className="btn" type="submit" disabled={saving}>
            {saving ? 'Saving...' : 'Save Profile'}
          </button>
        </form>

        <div style={{ marginTop: 20 }}>
          <button className="btn" type="button" onClick={openDeleteModal} disabled={deleting}>
            {deleting ? 'Deleting...' : 'Delete My Account'}
          </button>
        </div>
      </div>

      {showDeleteModal && (
        <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="delete-account-title">
          <div className="modal-card">
            <h2 id="delete-account-title">Delete Customer Account</h2>
            <p>
              This will permanently remove your customer account. Type <strong>DELETE</strong> to confirm.
            </p>
            <input
              type="text"
              className="auth-input"
              value={deleteConfirmationText}
              onChange={(event) => setDeleteConfirmationText(event.target.value)}
              placeholder="Type DELETE"
            />
            <div className="modal-actions">
              <button type="button" className="btn btn-secondary" onClick={closeDeleteModal} disabled={deleting}>
                Cancel
              </button>
              <button type="button" className="btn" onClick={handleDeleteAccount} disabled={deleting}>
                {deleting ? 'Deleting...' : 'Confirm Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
