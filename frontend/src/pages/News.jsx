
import { useEffect, useState } from "react";
import { getNews } from "../api/news";
import { getCompanies } from "../api/companies";
import {
    Newspaper, Search, RefreshCw, ExternalLink,
    AlertCircle
} from "lucide-react";

export default function News() {
    const [news, setNews] = useState([]);
    const [companies, setCompanies] = useState([]);
    const [search, setSearch] = useState("");
    const [companyId, setCompanyId] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [total, setTotal] = useState(0);
    const [skip, setSkip] = useState(0);
    const limit = 20;

    const fetchCompanies = async () => {
        try {
            const data = await getCompanies();
            setCompanies(Array.isArray(data) ? data : []);
        } catch (err) {
            console.error("Company loading failed:", err);
        }
    };

    const fetchNews = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await getNews({
                companyId: companyId || undefined,
                skip,
                limit,
            });

            setNews(data.news || []);
            setTotal(data.total || 0);
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Unable to load news."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCompanies();
    }, []);

    useEffect(() => {
        fetchNews();
    }, [companyId, skip]);

    const filteredNews = news.filter((item) =>
        item.headline?.toLowerCase().includes(search.toLowerCase()) ||
        item.source?.toLowerCase().includes(search.toLowerCase()) ||
        item.companies?.some((company) =>
            company.symbol?.toLowerCase().includes(search.toLowerCase())
        )
    );

    const formatDate = (date) => {
        if (!date) return "Date unavailable";

        const parsed = new Date(date);

        if (Number.isNaN(parsed.getTime())) {
            return "Date unavailable";
        }

        return parsed.toLocaleDateString();
    };

    return (
        <div className="space-y-6">

            <div className="flex justify-between items-center flex-wrap gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-white">
                        Financial News
                    </h1>
                    <p className="text-slate-400 text-sm mt-1">
                        News articles and automatic company categorization.
                    </p>
                </div>

                <button
                    onClick={fetchNews}
                    className="flex items-center gap-2 bg-blue-600 px-4 py-2 rounded-lg text-sm"
                >
                    <RefreshCw size={16} /> Refresh
                </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <Newspaper className="text-blue-400 mb-3" />
                    <p className="text-slate-400 text-sm">Total Articles</p>
                    <h2 className="text-3xl font-bold mt-1">{total}</h2>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <p className="text-slate-400 text-sm">Articles on This Page</p>
                    <h2 className="text-3xl font-bold mt-2">{news.length}</h2>
                </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative flex-1">
                    <Search
                        size={18}
                        className="absolute left-3 top-3 text-slate-500"
                    />
                    <input
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        placeholder="Search headlines, sources or symbols..."
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg py-3 pl-10 pr-4 outline-none focus:border-blue-500"
                    />
                </div>

                <select
                    value={companyId}
                    onChange={(e) => {
                        setCompanyId(e.target.value);
                        setSkip(0);
                    }}
                    className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 outline-none"
                >
                    <option value="">All Companies</option>
                    {companies.map((company) => (
                        <option key={company.id} value={company.id}>
                            {company.symbol}
                        </option>
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
                <p className="text-slate-400">Loading news...</p>
            ) : filteredNews.length === 0 ? (
                <div className="bg-slate-900 rounded-xl p-10 text-center text-slate-400">
                    No news articles found.
                </div>
            ) : (
                <div className="space-y-4">
                    {filteredNews.map((item) => (
                        <article
                            key={item.id}
                            className="bg-slate-900 border border-slate-800 rounded-xl p-5"
                        >
                            <div className="flex justify-between flex-wrap gap-2">
                <span className="text-xs text-blue-400 font-semibold">
                  {item.source || "Unknown source"}
                </span>

                                <span className="text-xs text-slate-500">
                  {formatDate(item.published_at)}
                </span>
                            </div>

                            <h2 className="text-lg font-semibold text-white mt-3">
                                {item.headline}
                            </h2>

                            <p className="text-sm text-slate-400 mt-3 leading-6">
                                {item.body || "No article description available."}
                            </p>

                            <div className="mt-4">
                                <p className="text-xs uppercase text-slate-500 mb-2">
                                    Associated Companies
                                </p>

                                <div className="flex flex-wrap gap-2">
                                    {(item.companies || []).map((company) => (
                                        <span
                                            key={company.company_id}
                                            className="bg-blue-500/10 text-blue-300 px-3 py-1 rounded-full text-xs"
                                        >
                      {company.symbol} ·{" "}
                                            {(company.confidence * 100).toFixed(0)}% confidence
                    </span>
                                    ))}

                                    {!item.companies?.length && (
                                        <span className="text-xs text-slate-500">
                      No company associations
                    </span>
                                    )}
                                </div>
                            </div>

                            {item.url && (
                                <a
                                    href={item.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center gap-2 mt-5 text-blue-400 text-sm hover:text-blue-300"
                                >
                                    Read original article
                                    <ExternalLink size={15} />
                                </a>
                            )}
                        </article>
                    ))}
                </div>
            )}

            <div className="flex justify-between items-center">
                <button
                    disabled={skip === 0 || loading}
                    onClick={() => setSkip((s) => Math.max(0, s - limit))}
                    className="px-4 py-2 bg-slate-800 rounded-lg disabled:opacity-30"
                >
                    Previous
                </button>

                <span className="text-sm text-slate-400">
          Showing {total === 0 ? 0 : skip + 1}–{Math.min(skip + limit, total)} of {total}
        </span>

                <button
                    disabled={skip + limit >= total || loading}
                    onClick={() => setSkip((s) => s + limit)}
                    className="px-4 py-2 bg-slate-800 rounded-lg disabled:opacity-30"
                >
                    Next
                </button>
            </div>

        </div>
    );
}
