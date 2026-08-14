import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { DashboardPage } from "./pages/Dashboard";
import { CreateAccountPage } from "./pages/CreateAccountPage";
import { AccountPage } from "./pages/AccountPage";
import { CreateTransactionPage } from "./pages/CreateTransactionPage";

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
        path="/accounts/:accountId/transaction"
        element={
          <ProtectedRoute>
            <CreateTransactionPage />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}