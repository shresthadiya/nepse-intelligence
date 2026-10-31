
import { useEffect, useState } from "react";
import { getCompanies } from "../api/companies";
import {
    Search, Building2, RefreshCw, AlertCircle,
    ArrowUpRight
} from "lucide-react";

export default function Companies() {
    const [companies, setCompanies] = useState([]);
    const [search, setSearch] = useState("");
    const [sector, setSector] = useState("All");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [selected, setSelected] = useState(null);

    const fetchCompanies = async () => {
        try {
            setLoading(true);
            setError("");
            const data = await getCompanies();
            setCompanies(Array.isArray(data) ? data : []);
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Unable to load companies."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCompanies();
    }, []);

    const sectors = [
        "All",
        ...new Set(companies.map((c) => c.sector).filter(Boolean))
    ];

    const filtered = companies.filter((company) => {
        const matchesSearch =
            company.name.toLowerCase().includes(search.toLowerCase()) ||
            company.symbol.toLowerCase().includes(search.toLowerCase());

        const matchesSector =
            sector === "All" || company.sector === sector;

        return matchesSearch && matchesSector;
    });

    return (
        <div className="space-y-6">

            <div className="flex flex-wrap justify-between items-center gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-white">
                        Companies
                    </h1>
                    <p className="text-slate-400 text-sm mt-1">
                        Explore tracked companies in the NEPSE market.
                    </p>
                </div>

                <button
                    onClick={fetchCompanies}
                    className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm"
                >
                    <RefreshCw size={16} />
                    Refresh
                </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <Building2 className="text-blue-400 mb-3" />
                    <p className="text-slate-400 text-sm">Total Companies</p>
                    <h2 className="text-3xl font-bold mt-1">
                        {companies.length}
                    </h2>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <p className="text-slate-400 text-sm">Active Companies</p>
                    <h2 className="text-3xl font-bold mt-2 text-green-400">
                        {companies.filter((c) => c.is_active).length}
                    </h2>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <p className="text-slate-400 text-sm">Sectors Represented</p>
                    <h2 className="text-3xl font-bold mt-2">
                        {new Set(companies.map((c) => c.sector)).size}
                    </h2>
                </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative flex-1">
                    <Search
                        className="absolute left-3 top-3 text-slate-500"
                        size={18}
                    />
                    <input
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        placeholder="Search by company name or symbol..."
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg py-3 pl-10 pr-4 outline-none focus:border-blue-500"
                    />
                </div>

                <select
                    value={sector}
                    onChange={(e) => setSector(e.target.value)}
                    className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 outline-none"
                >
                    {sectors.map((item) => (
                        <option key={item} value={item}>{item}</option>
                    ))}
                </select>
            </div>

            {error && (
                <div className="bg-red-500/10 text-red-400 p-4 rounded-lg">
                    <AlertCircle className="inline mr-2" size={18} />
                    {error}
                </div>
            )}

            {loading ? (
                <p className="text-slate-400">Loading companies...</p>
            ) : filtered.length === 0 ? (
                <div className="bg-slate-900 p-8 rounded-xl text-center text-slate-400">
                    No companies found.
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
                    {filtered.map((company) => (
                        <div
                            key={company.id}
                            className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-blue-500/60 transition"
                        >
                            <div className="flex justify-between items-start">
                                <div className="bg-blue-500/10 text-blue-400 p-3 rounded-lg font-bold">
                                    {company.symbol}
                                </div>

                                <span className={`text-xs px-2 py-1 rounded-full ${
                                    company.is_active
                                        ? "bg-green-500/10 text-green-400"
                                        : "bg-slate-700 text-slate-400"
                                }`}>
                  {company.is_active ? "Active" : "Inactive"}
                </span>
                            </div>

                            <h3 className="font-semibold text-white mt-5">
                                {company.name}
                            </h3>

                            <p className="text-sm text-slate-400 mt-2">
                                {company.sector || "Sector unavailable"}
                            </p>

                            <button
                                onClick={() => setSelected(company)}
                                className="mt-5 flex items-center gap-2 text-blue-400 text-sm hover:text-blue-300"
                            >
                                View details <ArrowUpRight size={16} />
                            </button>
                        </div>
                    ))}
                </div>
            )}

            {selected && (
                <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4">
                    <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-md w-full">
                        <div className="flex justify-between items-center mb-5">
                            <h2 className="text-xl font-bold">Company Details</h2>
                            <button onClick={() => setSelected(null)}>✕</button>
                        </div>

                        <p className="text-blue-400 font-bold text-lg">
                            {selected.symbol}
                        </p>
                        <p className="mt-2">{selected.name}</p>
                        <p className="text-slate-400 mt-2">
                            Sector: {selected.sector}
                        </p>
                        <p className="text-slate-400 mt-2">
                            ID: {selected.id}
                        </p>
                        <p className="text-slate-400 mt-2">
                            Status: {selected.is_active ? "Active" : "Inactive"}
                        </p>

                        <button
                            onClick={() => setSelected(null)}
                            className="mt-6 w-full bg-blue-600 py-2 rounded-lg"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}

        </div>
    );
}
