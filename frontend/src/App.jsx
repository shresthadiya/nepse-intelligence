import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./routes/ProtectedRoute";
import { useAuth } from "./context/AuthContext";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Companies from "./pages/Companies";
import News from "./pages/News";
import Analytics from "./pages/Analytics";
import Admin from "./pages/Admin";
import MainLayout from "./layouts/MainLayout";

export default function App() {
  const { isAuthenticated } = useAuth();

  return (
      <Routes>
        <Route
            path="/"
            element={
              <Navigate
                  to={isAuthenticated ? "/dashboard" : "/login"}
                  replace
              />
            }
        />

        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/news" element={<News />} />

            <Route
                element={
                  <ProtectedRoute
                      allowedRoles={["admin", "analyst"]}
                  />
                }
            >
              <Route path="/analytics" element={<Analytics />} />
            </Route>

            <Route
                element={
                  <ProtectedRoute allowedRoles={["admin"]} />
                }
            >
              <Route path="/admin" element={<Admin />} />
            </Route>
          </Route>
        </Route>

        <Route
            path="*"
            element={<Navigate to="/dashboard" replace />}
        />
      </Routes>
  );
}