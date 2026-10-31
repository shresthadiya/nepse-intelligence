import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import {
    LayoutDashboard,
    Building2,
    Newspaper,
    ChartNoAxesCombined,
    Settings,
    LogOut,
    TrendingUp,
    UserCircle,
} from "lucide-react";

export default function MainLayout() {
    const { user, logout, hasRole } = useAuth();
    const navigate = useNavigate();

    const navigation = [
        {
            name: "Dashboard",
            path: "/dashboard",
            icon: LayoutDashboard,
            roles: ["admin", "analyst", "viewer"],
        },
        {
            name: "Companies",
            path: "/companies",
            icon: Building2,
            roles: ["admin", "analyst", "viewer"],
        },
        {
            name: "News",
            path: "/news",
            icon: Newspaper,
            roles: ["admin", "analyst", "viewer"],
        },
        {
            name: "Analytics",
            path: "/analytics",
            icon: ChartNoAxesCombined,
            roles: ["admin", "analyst"],
        },
        {
            name: "Administration",
            path: "/admin",
            icon: Settings,
            roles: ["admin"],
        },
    ];

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex">

            {/* Sidebar */}

            <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col fixed inset-y-0 left-0 z-20">

                <div className="p-6 border-b border-slate-800">

                    <div className="flex items-center gap-3">
                        <div className="bg-blue-600 p-2 rounded-lg">
                            <TrendingUp size={22} />
                        </div>

                        <div>
                            <h1 className="font-bold text-lg">
                                NEPSE
                            </h1>

                            <p className="text-xs text-slate-400">
                                Intelligence
                            </p>
                        </div>
                    </div>

                </div>

                <nav className="flex-1 p-4 space-y-2">

                    <p className="text-xs uppercase tracking-wider text-slate-500 mb-4 px-3">
                        Main Menu
                    </p>

                    {navigation
                        .filter((item) => hasRole(...item.roles))
                        .map((item) => {
                            const Icon = item.icon;

                            return (
                                <NavLink
                                    key={item.path}
                                    to={item.path}
                                    className={({ isActive }) =>
                                        `flex items-center gap-3 px-3 py-3 rounded-lg text-sm transition ${
                                            isActive
                                                ? "bg-blue-600 text-white"
                                                : "text-slate-400 hover:bg-slate-800 hover:text-white"
                                        }`
                                    }
                                >
                                    <Icon size={19} />
                                    {item.name}
                                </NavLink>
                            );
                        })}

                </nav>

                <div className="p-4 border-t border-slate-800">

                    <div className="flex items-center gap-3 mb-4 px-2">
                        <UserCircle size={35} className="text-slate-400" />

                        <div className="overflow-hidden">
                            <p className="text-sm font-medium truncate">
                                {user?.username}
                            </p>

                            <p className="text-xs text-blue-400 capitalize">
                                {user?.role}
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={handleLogout}
                        className="flex items-center gap-3 text-slate-400 hover:text-red-400 px-3 py-2 w-full text-sm transition"
                    >
                        <LogOut size={18} />
                        Logout
                    </button>

                </div>

            </aside>

            {/* Main Content */}

            <main className="flex-1 ml-64 min-w-0">

                <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-8">

                    <div>
                        <p className="text-sm text-slate-400">
                            Stock Market Intelligence
                        </p>
                    </div>

                    <div className="flex items-center gap-3">
            <span className="text-sm text-slate-300">
              {user?.email}
            </span>

                        <span className="h-2 w-2 bg-green-400 rounded-full" />
                    </div>

                </header>

                <div className="p-8">
                    <Outlet />
                </div>

            </main>

        </div>
    );
}