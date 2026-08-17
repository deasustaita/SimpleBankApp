import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { createAccount } from "../api/accountApi";



export function CreateAccountPage() {
    const { customer } = useAuth();
    const navigate = useNavigate();

    const [accountType, setAccountType] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [balance, setBalance] = useState("");
    const [nickname, setNickname] = useState("");

    async function handleSubmit(event: React.FormEvent) {
        event.preventDefault();

        if (!customer) {
            setError("You must be logged in to create an account.");
            return;
        }

        setError("");
        setLoading(true);

        try {
            await createAccount(
                customer._id,
                accountType,
                balance === "" ? 0 : Number(balance),
                nickname
            );

            navigate("/dashboard");
        } catch (error) {
            setError(
                error instanceof Error
                    ? error.message
                    : "Unable to create account."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="page centered-page">
            <div className="panel form-panel">
                <h1>Open a New Account</h1>

                <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="accountType">
                        Account Type
                    </label>

                    <select
                        id="accountType"
                        value={accountType}
                        onChange={(event) =>
                            setAccountType(event.target.value)
                        }
                        required
                    >
                        <option value="">
                            Select an account type
                        </option>

                        <option value="CHECKING">
                            Checking
                        </option>

                        <option value="SAVINGS">
                            Savings
                        </option>
                    </select>
                </div>

                <div>
                    <label htmlFor="nickname">
                        Account Name (Optional)
                    </label>

                    <input
                        id="nickname"
                        type="text"
                        value={nickname}
                        onChange={(event) => setNickname(event.target.value)}
                        placeholder="Defaults to account type"
                    />
                </div>

                <div>
                    <label htmlFor="balance">
                        Starting Balance (Optional)
                    </label>

                    <input 
                        id="balance"
                        type="number"
                        min="0"
                        step="0.01"
                        value={balance}
                        onChange={(event) =>
                            setBalance(event.target.value)
                        }
                        placeholder="0.00"
                    />
                </div>

                    {error && <p className="error-text">{error}</p>}

                    <div className="action-row">
                        <button className="btn" type="submit" disabled={loading}>
                            {loading ? "Creating Account..." : "Create Account"}
                        </button>
                        <button className="btn btn-secondary" type="button" onClick={() => navigate("/dashboard")}>
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}