import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { Navbar } from "./components/common/Navbar";
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { DashboardPage } from "./pages/Dashboard";
import { CreateAccountPage } from "./pages/CreateAccountPage";
import { AccountPage } from "./pages/AccountPage";
import { AccountsPage } from "./pages/AccountsPage";
import { AccountSettingsPage } from "./pages/AccountSettingsPage";
import { CreateTransactionPage } from "./pages/CreateTransactionPage";
import { TransactionsPage } from "./pages/TransactionsPage";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { customer, loading } = useAuth();

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!customer) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />

      <Route 
        path="/accounts"
        element={
          <ProtectedRoute>
            <AccountsPage />
          </ProtectedRoute>
        }
      />

      <Route 
        path="/accounts/create"
        element={
          <ProtectedRoute>
            <CreateAccountPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/accounts/:accountId"
        element={
          <ProtectedRoute>
            <AccountPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/accounts/:accountId/settings"
        element={
          <ProtectedRoute>
            <AccountSettingsPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/accounts/:accountId/transaction"
        element={
          <ProtectedRoute>
            <CreateTransactionPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/transactions"
        element={
          <ProtectedRoute>
            <TransactionsPage />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}