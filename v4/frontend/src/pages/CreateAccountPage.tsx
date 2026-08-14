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
                balance === "" ? 0 : Number(balance)
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
        <div>
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

                {error && (
                    <p>{error}</p>
                )}

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Creating Account..."
                        : "Create Account"}
                </button>
            </form>

            <button onClick={() => navigate("/dashboard")}>
                Cancel
            </button>
        </div>
    );
}