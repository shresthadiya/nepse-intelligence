import {
    createContext,
    useContext,
    useState,
} from "react";

import {
    loginUser,
    getCurrentUser,
} from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(() => {
        try {
            return JSON.parse(localStorage.getItem("user")) || null;
        } catch {
            return null;
        }
    });

    const [loading, setLoading] = useState(false);

    const login = async (email, password) => {
        setLoading(true);

        try {
            const tokenData = await loginUser(email, password);

            localStorage.setItem(
                "access_token",
                tokenData.access_token
            );

            const userData = await getCurrentUser();

            localStorage.setItem("user", JSON.stringify(userData));
            setUser(userData);

            return userData;
        } catch (error) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");
            setUser(null);

            throw error;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        setUser(null);
    };

    const hasRole = (...roles) => {
        return Boolean(user && roles.includes(user.role));
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                logout,
                hasRole,
                isAuthenticated: Boolean(user),
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);