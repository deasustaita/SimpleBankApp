import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function LoginPage() {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event: React.FormEvent) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await login(username, password);

            navigate("/dashboard");
        } catch (error) {
            setError(
                error instanceof Error
                    ? error.message
                    : "Login failed."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="auth-shell">
            <section className="auth-card">
                <p className="auth-kicker">Simple Bank</p>
                <h1>Welcome Back</h1>
                <p className="auth-subtitle">Sign in to manage your money securely.</p>

                <form className="auth-form" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            className="auth-input"
                            type="text"
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            className="auth-input"
                            type="password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            required
                        />
                    </div>

                    {error && <p className="error-text">{error}</p>}

                    <button className="btn auth-submit" type="submit" disabled={loading}>
                        {loading ? "Logging in..." : "Sign In"}
                    </button>
                </form>

                <p className="auth-footnote">
                    Don't have an account? <Link to="/register">Create one</Link>
                </p>
            </section>
        </main>
    );
}