import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

export function LandingPage() {
    const { customer, loading } = useAuth();

    if (!loading && customer) {
        return <Navigate to="/dashboard" replace />;
    }

    return (
        <div>
            <section className="hero">
                <h1>Welcome to SimpleBank</h1>
                <p>
                    Manage checking and savings accounts, track transactions, and keep your
                    finances organized in one simple place.
                </p>
                <div className="btn-group" style={{ justifyContent: "center" }}>
                    <Link className="btn" to="/register">
                        Get Started
                    </Link>
                    <Link className="btn btn-secondary" to="/login">
                        Sign In
                    </Link>
                </div>
            </section>

            <div className="page">
                <div className="grid">
                    <div className="card">
                        <h3>Checking Accounts</h3>
                        <p>
                            Everyday spending with built-in overdraft coverage so you're never
                            caught short.
                        </p>
                    </div>
                    <div className="card">
                        <h3>Savings Accounts</h3>
                        <p>
                            Set money aside and watch it grow, safe from accidental overdrafts.
                        </p>
                    </div>
                    <div className="card">
                        <h3>Simple Transfers</h3>
                        <p>
                            Deposit, withdraw, and transfer funds between accounts in just a
                            couple of clicks.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
