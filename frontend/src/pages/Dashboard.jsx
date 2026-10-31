
import { useEffect, useState } from "react";
import {
    TrendingUp,
    TrendingDown,
    Building2,
    Newspaper,
    Activity,
    RefreshCw,
    BarChart3,
    Clock,
} from "lucide-react";

const API_URL = "http://localhost:8000";

function StatCard({ title, value, subtitle, icon: Icon }) {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex justify-between items-center">
                <p className="text-slate-400 text-sm">{title}</p>
                <Icon size={20} className="text-blue-400" />
            </div>
            <h2 className="text-2xl font-bold mt-4 text-white">
                {value}
            </h2>
            <p className="text-slate-500 text-xs mt-2">{subtitle}</p>
        </div>
    );
}

export default function Dashboard() {
    const [companies, setCompanies] = useState([]);
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function fetchDashboardData() {
            setLoading(true);
            setError("");

            try {
                const [companyResponse, newsResponse] =
                    await Promise.all([
                        fetch(`${API_URL}/api/companies/`),
                        fetch(`${API_URL}/api/news/`),
                    ]);

                if (!companyResponse.ok || !newsResponse.ok) {
                    throw new Error("Unable to load dashboard data.");
                }

                const companyData = await companyResponse.json();
                const newsData = await newsResponse.json();

                setCompanies(
                    Array.isArray(companyData)
                        ? companyData
                        : companyData.items || []
                );

                setNews(
                    Array.isArray(newsData)
                        ? newsData
                        : newsData.items || []
                );
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchDashboardData();
    }, []);

    return (
        <div className="space-y-8 text-white">

            {/* Header */}
            <div className="flex flex-wrap justify-between items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold">
                        Dashboard
                    </h1>
                    <p className="text-slate-400 mt-2">
                        Market overview and stock intelligence.
                    </p>
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-400">
                    <Activity size={16} className="text-green-400" />
                    NEPSE Intelligence
                </div>
            </div>

            {error && (
                <div className="bg-red-950/40 border border-red-800 rounded-lg p-4 text-red-300">
                    {error}
                </div>
            )}

            {/* Market Overview */}
            <section>
                <h2 className="text-lg font-semibold mb-4">
                    Market Overview
                </h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
                    <StatCard
                        title="NEPSE Index"
                        value="--"
                        subtitle="Market index data unavailable"
                        icon={BarChart3}
                    />

                    <StatCard
                        title="Total Companies"
                        value={companies.length}
                        subtitle="Registered companies"
                        icon={Building2}
                    />

                    <StatCard
                        title="Market News"
                        value={news.length}
                        subtitle="Available news articles"
                        icon={Newspaper}
                    />

                    <StatCard
                        title="Market Movement"
                        value="--"
                        subtitle="Awaiting stock price data"
                        icon={TrendingUp}
                    />
                </div>
            </section>

            {/* Market Performance */}
            <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h2 className="text-lg font-semibold">
                            Market Performance
                        </h2>
                        <p className="text-sm text-slate-400 mt-1">
                            NEPSE index historical performance
                        </p>
                    </div>
                    <BarChart3 className="text-blue-400" />
                </div>

                <div className="h-56 flex flex-col items-center justify-center text-slate-500">
                    <Activity size={40} className="mb-3" />
                    <p>No historical market data available.</p>
                    <p className="text-xs mt-2">
                        Stock price integration is pending.
                    </p>
                </div>
            </section>

            {/* Companies and News */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

                {/* Companies */}
                <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-5">
                        <h2 className="text-lg font-semibold">
                            Listed Companies
                        </h2>
                        <Building2 className="text-blue-400" />
                    </div>

                    {loading ? (
                        <p className="text-slate-400">Loading companies...</p>
                    ) : companies.length === 0 ? (
                        <p className="text-slate-500">
                            No companies available.
                        </p>
                    ) : (
                        <div className="space-y-4">
                            {companies.slice(0, 6).map((company, index) => (
                                <div
                                    key={company.id || index}
                                    className="flex justify-between items-center border-b border-slate-800 pb-3"
                                >
                                    <div>
                                        <p className="font-medium">
                                            {company.symbol || company.name}
                                        </p>
                                        <p className="text-xs text-slate-500">
                                            {company.name}
                                        </p>
                                    </div>
                                    <span className="text-xs text-green-400">
                                        Registered
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}
                </section>

                {/* News */}
                <section className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-5">
                        <h2 className="text-lg font-semibold">
                            Latest Market News
                        </h2>
                        <Newspaper className="text-blue-400" />
                    </div>

                    {loading ? (
                        <p className="text-slate-400">Loading news...</p>
                    ) : news.length === 0 ? (
                        <p className="text-slate-500">
                            No news articles available.
                        </p>
                    ) : (
                        <div className="space-y-4">
                            {news.slice(0, 5).map((article, index) => (
                                <div
                                    key={article.id || index}
                                    className="border-b border-slate-800 pb-3"
                                >
                                    <p className="font-medium text-sm">
                                        {article.title}
                                    </p>
                                    <div className="flex items-center gap-2 mt-2 text-xs text-slate-500">
                                        <Clock size={13} />
                                        {article.published_at
                                            ? new Date(
                                                article.published_at
                                            ).toLocaleDateString()
                                            : "Recently added"}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </section>
            </div>

            {/* Gainers and Losers */}
            <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex gap-2 items-center mb-4">
                        <TrendingUp className="text-green-400" />
                        <h2 className="font-semibold">Top Gainers</h2>
                    </div>
                    <p className="text-sm text-slate-500">
                        Awaiting stock price data.
                    </p>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex gap-2 items-center mb-4">
                        <TrendingDown className="text-red-400" />
                        <h2 className="font-semibold">Top Losers</h2>
                    </div>
                    <p className="text-sm text-slate-500">
                        Awaiting stock price data.
                    </p>
                </div>
            </section>

            <div className="text-xs text-slate-600 flex items-center gap-2">
                <RefreshCw size={13} />
                Dashboard data is retrieved from the backend API.
            </div>
        </div>
    );
}
