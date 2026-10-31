
import { useState } from "react";
import { triggerCrawl } from "../api/analytics";
import { useAuth } from "../context/AuthContext";

import {
    Settings,
    Database,
    Play,
    ShieldCheck,
    AlertCircle,
    CheckCircle,
    LoaderCircle,
    User,
} from "lucide-react";

export default function Admin() {
    const { user, hasRole } = useAuth();

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const handleCrawl = async () => {
        if (!window.confirm("Do you want to trigger a crawl run?")) {
            return;
        }

        try {
            setLoading(true);
            setError("");
            setResult(null);

            const response = await triggerCrawl();

            setResult(response);
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Unable to trigger crawl. Please try again."
            );
        } finally {
            setLoading(false);
        }
    };

    if (!hasRole("admin")) {
        return (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-8 text-center">
                <ShieldCheck
                    size={40}
                    className="text-red-400 mx-auto mb-4"
                />

                <h2 className="text-xl font-bold text-white">
                    Access Denied
                </h2>

                <p className="text-slate-400 mt-2">
                    Only administrators can access this page.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-6">

            <div>
                <h1 className="text-2xl font-bold flex items-center gap-3">
                    <Settings className="text-blue-400" />
                    Administration
                </h1>

                <p className="text-slate-400 text-sm mt-2">
                    Manage administrative operations and data collection.
                </p>
            </div>

            {/* Admin Profile */}

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

                <div className="flex items-center gap-3 mb-4">
                    <User className="text-blue-400" />
                    <h2 className="font-semibold">
                        Administrator Account
                    </h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <div>
                        <p className="text-xs text-slate-500">Username</p>
                        <p className="mt-1 font-medium">{user?.username}</p>
                    </div>

                    <div>
                        <p className="text-xs text-slate-500">Email</p>
                        <p className="mt-1 font-medium">{user?.email}</p>
                    </div>

                    <div>
                        <p className="text-xs text-slate-500">Role</p>
                        <p className="mt-1 text-blue-400 font-medium capitalize">
                            {user?.role}
                        </p>
                    </div>

                </div>
            </div>

            {/* Crawler Management */}

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">

                <div className="flex items-center gap-3 mb-4">
                    <Database className="text-blue-400" size={24} />

                    <div>
                        <h2 className="text-lg font-semibold">
                            Crawler Management
                        </h2>

                        <p className="text-sm text-slate-400">
                            Trigger collection of market and financial news data.
                        </p>
                    </div>
                </div>

                <div className="bg-slate-950 border border-slate-800 rounded-lg p-5">

                    <div className="flex flex-wrap justify-between items-center gap-4">

                        <div>
                            <h3 className="font-medium text-white">
                                Start Crawl Run
                            </h3>

                            <p className="text-sm text-slate-400 mt-1">
                                Request a new crawl through the backend API.
                            </p>
                        </div>

                        <button
                            onClick={handleCrawl}
                            disabled={loading}
                            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-5 py-3 rounded-lg text-sm font-medium"
                        >
                            {loading ? (
                                <>
                                    <LoaderCircle size={17} className="animate-spin" />
                                    Starting...
                                </>
                            ) : (
                                <>
                                    <Play size={17} />
                                    Trigger Crawl
                                </>
                            )}
                        </button>

                    </div>

                </div>

                {error && (
                    <div className="mt-5 bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-lg">
                        <AlertCircle className="inline mr-2" size={18} />
                        {error}
                    </div>
                )}

                {result !== null && (
                    <div className="mt-5 bg-green-500/10 border border-green-500/30 rounded-lg p-5">

                        <div className="flex items-center gap-2 text-green-400 mb-3">
                            <CheckCircle size={19} />
                            <h3 className="font-semibold">
                                Crawl request response received
                            </h3>
                        </div>

                    </div>
                )}

            </div>

            {/* Access Information */}

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

                <div className="flex items-center gap-3 mb-3">
                    <ShieldCheck className="text-green-400" />
                    <h2 className="font-semibold">
                        Role-Based Access Control
                    </h2>
                </div>

                <p className="text-sm text-slate-400 leading-6">
                    Administrative operations are protected by backend
                    authorization. Only users with the administrator role
                    should be able to manage crawler operations and other
                    restricted resources.
                </p>

            </div>

        </div>
    );
}
