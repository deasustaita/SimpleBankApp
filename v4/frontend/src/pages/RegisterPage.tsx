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
        <div>
            <h1>SimpleBank</h1>

            <h2>Create Account</h2>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name</label>

                    <input
                        type="text"
                        value={name}
                        onChange={(event) => setName(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Email</label>

                    <input
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Username</label>

                    <input
                        type="text"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label>Password</label>

                    <input
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />
                </div>

                {error && (
                    <p>{error}</p>
                )}

                <button type="submit" disabled={loading}>
                    {loading ? "Creating account..." : "Register"}
                </button>
            </form>

            <p>
                Already have an account?{" "}
                <Link to="/login">
                    Login
                </Link>
            </p>
        </div>
    );
}