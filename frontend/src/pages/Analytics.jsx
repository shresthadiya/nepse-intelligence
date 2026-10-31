
import { useEffect, useState } from "react";
import {
    getCompanies,
    getCompanyPrices,
    getCompanyBehavior,
} from "../api/companies";

import {
    ChartNoAxesCombined,
    RefreshCw,
    Activity,
    Database,
    AlertCircle,
} from "lucide-react";

function DataPanel({ title, icon: Icon, data }) {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center gap-3 mb-4">
                <Icon size={20} className="text-blue-400" />
                <h2 className="font-semibold">{title}</h2>
            </div>

            {data === null || data === undefined ? (
                <p className="text-slate-500 text-sm">No data available.</p>
            ) : (
                <pre className="text-xs text-slate-300 whitespace-pre-wrap break-words overflow-auto max-h-96 leading-6">
          {JSON.stringify(data, null, 2)}
        </pre>
            )}
        </div>
    );
}

export default function Analytics() {
    const [companies, setCompanies] = useState([]);
    const [companyId, setCompanyId] = useState("");
    const [prices, setPrices] = useState(null);
    const [behavior, setBehavior] = useState(null);
    const [range, setRange] = useState("30d");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadCompanies = async () => {
            try {
                const data = await getCompanies();
                setCompanies(Array.isArray(data) ? data : []);

                if (data.length > 0) {
                    setCompanyId(String(data[0].id));
                }
            } catch (err) {
                setError("Unable to load companies.");
            }
        };

        loadCompanies();
    }, []);

    const fetchAnalytics = async () => {
        if (!companyId) return;

        try {
            setLoading(true);
            setError("");
            setPrices(null);
            setBehavior(null);

            const [priceResult, behaviorResult] =
                await Promise.allSettled([
                    getCompanyPrices(companyId, range),
                    getCompanyBehavior(companyId),
                ]);

            if (priceResult.status === "fulfilled") {
                setPrices(priceResult.value);
            }

            if (behaviorResult.status === "fulfilled") {
                setBehavior(behaviorResult.value);
            }

            if (
                priceResult.status === "rejected" &&
                behaviorResult.status === "rejected"
            ) {
                setError("Unable to load stock analytics.");
            }
        } catch (err) {
            setError("An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (companyId) {
            fetchAnalytics();
        }
    }, [companyId, range]);

    const selectedCompany = companies.find(
        (company) => String(company.id) === companyId
    );

    return (
        <div className="space-y-6">

            <div className="flex flex-wrap justify-between items-center gap-4">
                <div>
                    <h1 className="text-2xl font-bold">
                        Stock Analytics
                    </h1>

                    <p className="text-sm text-slate-400 mt-1">
                        Company price data and buyer/seller behavior analysis.
                    </p>
                </div>

                <button
                    onClick={fetchAnalytics}
                    disabled={loading || !companyId}
                    className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-4 py-2 rounded-lg"
                >
                    <RefreshCw size={16} />
                    Refresh
                </button>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                    <div>
                        <label className="block text-sm text-slate-400 mb-2">
                            Select Company
                        </label>

                        <select
                            value={companyId}
                            onChange={(e) => setCompanyId(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 outline-none"
                        >
                            {companies.map((company) => (
                                <option key={company.id} value={company.id}>
                                    {company.symbol} - {company.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm text-slate-400 mb-2">
                            Price Range
                        </label>

                        <select
                            value={range}
                            onChange={(e) => setRange(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 outline-none"
                        >
                            <option value="7d">Last 7 days</option>
                            <option value="30d">Last 30 days</option>
                            <option value="90d">Last 90 days</option>
                        </select>
                    </div>

                </div>
            </div>

            {selectedCompany && (
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <p className="text-sm text-slate-400">Currently analyzing</p>
                    <h2 className="text-2xl font-bold text-blue-400 mt-2">
                        {selectedCompany.symbol}
                    </h2>
                    <p className="text-slate-400 mt-1">
                        {selectedCompany.name}
                    </p>
                </div>
            )}

            {error && (
                <div className="bg-red-500/10 text-red-400 p-4 rounded-lg">
                    <AlertCircle className="inline mr-2" size={18} />
                    {error}
                </div>
            )}

            {loading ? (
                <div className="bg-slate-900 rounded-xl p-10 text-center text-slate-400">
                    Loading analytics...
                </div>
            ) : (
                <>
                    <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
                        <DataPanel
                            title="Stock Price Data"
                            icon={ChartNoAxesCombined}
                            data={prices}
                        />

                        <DataPanel
                            title="Behavior Analysis"
                            icon={Activity}
                            data={behavior}
                        />
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                        <div className="flex items-center gap-3 mb-3">
                            <Database className="text-blue-400" size={20} />
                            <h2 className="font-semibold">
                                Analysis Information
                            </h2>
                        </div>

                        <p className="text-sm text-slate-400 leading-6">
                            The stock price endpoint supplies historical price
                            information, while the behavior summary endpoint
                            supplies the available buyer/seller analysis.
                            Values are displayed directly from the backend.
                            Missing data is not replaced with fabricated figures.
                        </p>
                    </div>
                </>
            )}

        </div>
    );
}
