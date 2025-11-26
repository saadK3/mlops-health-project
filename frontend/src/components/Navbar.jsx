import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Home, User, ShieldAlert, Activity } from "lucide-react";

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="w-full bg-white/80 backdrop-blur-md shadow-lg py-4 px-4 md:px-8 flex justify-between items-center sticky top-0 z-50 border-b border-slate-200/50">
      <Link to="/" className="flex items-center gap-2 group">
        <div className="p-2 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl group-hover:scale-110 transition-transform">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-xl md:text-2xl font-black bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
          HealthGuard AI
        </h1>
      </Link>

      <div className="flex gap-2 md:gap-4 items-center">
        <Link
          to="/"
          className={`px-4 py-2 rounded-xl font-semibold text-sm transition-all duration-200 flex items-center gap-2 ${
            isActive("/")
              ? "bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg"
              : "text-slate-700 hover:bg-slate-100"
          }`}
        >
          <Home className="w-4 h-4" />
          <span className="hidden sm:inline">Home</span>
        </Link>

        <Link
          to="/citizen"
          className={`px-4 py-2 rounded-xl font-semibold text-sm transition-all duration-200 flex items-center gap-2 ${
            isActive("/citizen")
              ? "bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg"
              : "text-slate-700 hover:bg-slate-100"
          }`}
        >
          <User className="w-4 h-4" />
          <span className="hidden sm:inline">Citizen</span>
        </Link>

        <Link
          to="/authority"
          className={`px-4 py-2 rounded-xl font-semibold text-sm transition-all duration-200 flex items-center gap-2 ${
            isActive("/authority")
              ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg"
              : "text-slate-700 hover:bg-slate-100"
          }`}
        >
          <ShieldAlert className="w-4 h-4" />
          <span className="hidden sm:inline">Authority</span>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
