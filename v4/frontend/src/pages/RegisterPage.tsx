import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function RegisterPage() {
    const { register } = useAuth();
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event: React.FormEvent) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await register(
                username,
                password,
                name,
                email
            );

            navigate("/dashboard");
        } catch (error) {
            setError(
                error instanceof Error
                    ? error.message
                    : "Registration failed."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="auth-shell">
            <section className="auth-card">
                <p className="auth-kicker">Simple Bank</p>
                <h1>Create Your Account</h1>
                <p className="auth-subtitle">Start banking with a faster, simpler dashboard.</p>

                <form className="auth-form" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="name">Name</label>
                        <input
                            id="name"
                            className="auth-input"
                            type="text"
                            value={name}
                            onChange={(event) => setName(event.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            className="auth-input"
                            type="email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                        />
                    </div>

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
                        {loading ? "Creating account..." : "Create Account"}
                    </button>
                </form>

                <p className="auth-footnote">
                    Already have an account? <Link to="/login">Sign in</Link>
                </p>
            </section>
        </main>
    );
}