import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { useEffect, useState } from "react";

export function Navbar() {
    const { customer, logout } = useAuth();
    const navigate = useNavigate();
    const [theme, setTheme] = useState<"light" | "dark">("light");

    useEffect(() => {
        const savedTheme = localStorage.getItem("sb_theme");
        const initialTheme =
            savedTheme === "dark" || savedTheme === "light"
                ? savedTheme
                : window.matchMedia("(prefers-color-scheme: dark)").matches
                  ? "dark"
                  : "light";

        document.documentElement.setAttribute("data-theme", initialTheme);
        setTheme(initialTheme);
    }, []);

    function toggleTheme() {
        const nextTheme = theme === "dark" ? "light" : "dark";
        setTheme(nextTheme);
        localStorage.setItem("sb_theme", nextTheme);
        document.documentElement.setAttribute("data-theme", nextTheme);
    }

    function handleLogout() {
        logout();
        navigate("/");
    }

    return (
        <nav className="navbar">
            <Link to={customer ? "/dashboard" : "/"} className="navbar-brand">
                Simple Bank
            </Link>

            <div className="navbar-links">
                <button className="btn btn-secondary" onClick={toggleTheme}>
                    {theme === "dark" ? "Light Mode" : "Dark Mode"}
                </button>
                {customer ? (
                    <>
                        <span className="navbar-greeting">Hi, {customer.name}</span>
                        <Link className="btn btn-secondary" to="/settings">
                            Profile
                        </Link>
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
