import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export function Navbar() {
    const { customer, logout } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate("/");
    }

    return (
        <nav className="navbar">
            <Link to={customer ? "/dashboard" : "/"} className="navbar-brand">
                SimpleBank
            </Link>

            <div className="navbar-links">
                {customer ? (
                    <>
                        <span className="navbar-greeting">Hi, {customer.name}</span>
                        <button className="btn btn-secondary" onClick={handleLogout}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link className="btn btn-secondary" to="/login">
                            Sign In
                        </Link>
                        <Link className="btn" to="/register">
                            Sign Up
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
}
