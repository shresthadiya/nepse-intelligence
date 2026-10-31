import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import {
    TrendingUp,
    LockKeyhole,
    Mail,
    Eye,
    EyeOff,
} from "lucide-react";

export default function Login() {
    const { login, loading } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            await login(email, password);
            navigate("/dashboard");
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Login failed. Please check your credentials."
            );
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">

            <div className="w-full max-w-md">

                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center bg-blue-600 p-3 rounded-xl mb-4">
                        <TrendingUp size={30} />
                    </div>

                    <h1 className="text-3xl font-bold text-white">
                        NEPSE Intelligence
                    </h1>

                    <p className="text-slate-400 mt-2">
                        Stock Market Analytics Platform
                    </p>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">

                    <h2 className="text-xl font-semibold text-white mb-2">
                        Welcome back
                    </h2>

                    <p className="text-slate-400 text-sm mb-6">
                        Sign in to access your dashboard.
                    </p>

                    {error && (
                        <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm mb-5">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">

                        <div>
                            <label className="block text-sm text-slate-300 mb-2">
                                Email address
                            </label>

                            <div className="relative">
                                <Mail
                                    size={18}
                                    className="absolute left-3 top-3 text-slate-500"
                                />

                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="admin@example.com"
                                    required
                                    className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-10 pr-4 text-white outline-none focus:border-blue-500"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm text-slate-300 mb-2">
                                Password
                            </label>

                            <div className="relative">
                                <LockKeyhole
                                    size={18}
                                    className="absolute left-3 top-3 text-slate-500"
                                />

                                <input
                                    type={showPassword ? "text" : "password"}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter your password"
                                    required
                                    className="w-full bg-slate-950 border border-slate-700 rounded-lg py-3 pl-10 pr-12 text-white outline-none focus:border-blue-500"
                                />

                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-3 text-slate-500"
                                >
                                    {showPassword ? (
                                        <EyeOff size={18} />
                                    ) : (
                                        <Eye size={18} />
                                    )}
                                </button>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold py-3 rounded-lg transition"
                        >
                            {loading ? "Signing in..." : "Sign In"}
                        </button>

                    </form>

                </div>

                <p className="text-center text-slate-600 text-xs mt-6">
                    NEPSE Intelligence © 2026
                </p>

            </div>
        </div>
    );
}