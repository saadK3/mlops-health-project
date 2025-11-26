import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import {
  AlertTriangle,
  Activity,
  Wind,
  TrendingUp,
  CheckCircle2,
  XCircle,
  Zap,
  Shield,
  Users,
  RefreshCw,
  Home,
  ArrowLeft,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "../components/Card";
import Navbar from "../components/Navbar";
import { Link } from "react-router-dom";

const AuthorityDashboard = () => {
  const [spatialRisk, setSpatialRisk] = useState([]);
  const [operationalStress, setOperationalStress] = useState([]);
  const [environmentalTriggers, setEnvironmentalTriggers] = useState([]);
  const [modelValidation, setModelValidation] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchAllData();
    setRefreshing(false);
    setLastRefresh(new Date());
  };

  const fetchAllData = async () => {
    try {
      const [spatial, stress, env, validation] = await Promise.all([
        axios.get("http://localhost:5000/api/authority/spatial-risk"),
        axios.get("http://localhost:5000/api/authority/operational-stress"),
        axios.get("http://localhost:5000/api/authority/environmental-triggers"),
        axios.get("http://localhost:5000/api/authority/model-validation"),
      ]);

      setSpatialRisk(spatial.data);
      setOperationalStress(stress.data);
      setEnvironmentalTriggers(
        env.data.map((item) => ({
          ...item,
          date: new Date(item.timestamp).toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
          }),
        }))
      );
      setModelValidation(validation.data.slice(0, 10).reverse());
      setLoading(false);
      setLastRefresh(new Date());
    } catch (err) {
      console.error("Failed to fetch authority data", err);
      setLoading(false);
    }
  };

  const getStressColor = (level) => {
    return level === "High"
      ? "text-red-700 bg-red-50"
      : "text-emerald-700 bg-emerald-50";
  };

  const totalRegions = spatialRisk.length;
  const criticalRegions = spatialRisk.filter((r) => r.avg_admissions > 15).length;
  const avgOccupancy =
    operationalStress.length > 0
      ? (
          (operationalStress.reduce((sum, s) => sum + s.avg_occupancy, 0) /
            operationalStress.length) *
          100
        ).toFixed(1)
      : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      {/* Top Navbar */}
      <Navbar />

      {/* Main page container */}
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-10">
        {/* Big white dashboard card */}
        <div className="bg-white rounded-3xl shadow-xl p-6 md:p-8 space-y-10">
          {/* Header with Stats */}
          <header className="animate-fade-in space-y-6">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <Link 
                    to="/" 
                    className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                  >
                    <ArrowLeft className="w-5 h-5 text-slate-600" />
                  </Link>
                  <h1 className="text-4xl md:text-5xl font-black gradient-text tracking-tight">
                    Authority Command Center
                  </h1>
                </div>
                <p className="text-slate-600 text-lg">
                  Real-time health surveillance and operational intelligence
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  Last updated: {lastRefresh.toLocaleTimeString()}
                </p>
              </div>
              <div className="flex gap-3 flex-wrap">
                <button
                  onClick={handleRefresh}
                  disabled={refreshing}
                  className="glass-dark text-white px-6 py-3 rounded-2xl flex items-center gap-3 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
                  <span>{refreshing ? 'Refreshing...' : 'Refresh Data'}</span>
                </button>
                <div className="glass-dark text-white px-6 py-3 rounded-2xl flex items-center gap-3 font-semibold shadow-lg animate-pulse-slow">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                  <span>System Active</span>
                </div>
              </div>
            </div>

            {/* Quick Stats cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card
                hover={false}
                className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white border-0 card-hover"
              >
                <CardContent className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100 text-sm font-medium mb-1">
                      Total Regions
                    </p>
                    <p className="text-4xl font-black">{totalRegions}</p>
                  </div>
                  <Users className="w-12 h-12 opacity-40" />
                </CardContent>
              </Card>

              <Card
                hover={false}
                className="bg-gradient-to-br from-orange-500 to-red-500 text-white border-0 card-hover"
              >
                <CardContent className="flex items-center justify-between">
                  <div>
                    <p className="text-orange-100 text-sm font-medium mb-1">
                      Critical Alerts
                    </p>
                    <p className="text-4xl font-black">{criticalRegions}</p>
                  </div>
                  <AlertTriangle className="w-12 h-12 opacity-40" />
                </CardContent>
              </Card>

              <Card
                hover={false}
                className="bg-gradient-to-br from-emerald-500 to-teal-500 text-white border-0 card-hover"
              >
                <CardContent className="flex items-center justify-between">
                  <div>
                    <p className="text-emerald-100 text-sm font-medium mb-1">
                      Avg Occupancy
                    </p>
                    <p className="text-4xl font-black">{avgOccupancy}%</p>
                  </div>
                  <Activity className="w-12 h-12 opacity-40" />
                </CardContent>
              </Card>
            </div>
          </header>

          {/* Spatial Risk */}
          <section className="animate-slide-up">
            <Card className="border-l-4 border-l-blue-500 bg-slate-50">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-blue-500 rounded-xl shadow-lg">
                    <Shield className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-2xl">
                      Spatial Risk Analysis
                    </CardTitle>
                    <p className="text-sm text-slate-600 mt-1">
                      Hospital admissions by region and population density
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {spatialRisk.length === 0 ? (
                  <div className="text-center py-16 text-slate-500">
                    <Activity className="w-16 h-16 mx-auto mb-4 opacity-30 animate-pulse" />
                    <p className="text-lg">Loading spatial risk data...</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b-2 border-slate-200/60 bg-slate-100">
                          <th className="text-left py-3 px-4 font-bold text-slate-700">
                            Region
                          </th>
                          <th className="text-left py-3 px-4 font-bold text-slate-700">
                            Density
                          </th>
                          <th className="text-right py-3 px-4 font-bold text-slate-700">
                            Avg Admissions
                          </th>
                          <th className="text-right py-3 px-4 font-bold text-slate-700">
                            Data Points
                          </th>
                          <th className="text-center py-3 px-4 font-bold text-slate-700">
                            Risk Level
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {spatialRisk.map((item, idx) => (
                          <tr
                            key={idx}
                            className="border-b border-slate-100 hover:bg-white transition-all duration-150"
                          >
                            <td className="py-3 px-4 font-semibold text-slate-900">
                              {item.region}
                            </td>
                            <td className="py-3 px-4">
                              <span
                                className={`px-3 py-1 rounded-full text-xs font-bold shadow-sm ${
                                  item.population_density === "Urban"
                                    ? "bg-gradient-to-r from-orange-400 to-red-400 text-white"
                                    : item.population_density === "Suburban"
                                    ? "bg-gradient-to-r from-yellow-400 to-orange-400 text-white"
                                    : "bg-gradient-to-r from-green-400 to-emerald-400 text-white"
                                }`}
                              >
                                {item.population_density}
                              </span>
                            </td>
                            <td className="py-3 px-4 text-right font-bold text-lg text-slate-900">
                              {item.avg_admissions}
                            </td>
                            <td className="py-3 px-4 text-right text-slate-600 font-medium">
                              {item.prediction_count}
                            </td>
                            <td className="py-3 px-4 text-center">
                              <span
                                className={`px-4 py-1.5 rounded-xl text-xs font-black shadow-md ${
                                  item.avg_admissions > 15
                                    ? "bg-gradient-to-r from-red-500 to-pink-500 text-white"
                                    : item.avg_admissions > 10
                                    ? "bg-gradient-to-r from-orange-500 to-yellow-500 text-white"
                                    : "bg-gradient-to-r from-emerald-500 to-teal-500 text-white"
                                }`}
                              >
                                {item.avg_admissions > 15
                                  ? "🔴 CRITICAL"
                                  : item.avg_admissions > 10
                                  ? "🟡 ELEVATED"
                                  : "🟢 NORMAL"}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </CardContent>
            </Card>
          </section>

          {/* Operational Stress */}
          <section className="animate-slide-up" style={{ animationDelay: "0.1s" }}>
            <Card className="border-l-4 border-l-orange-500 bg-amber-50/60">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-orange-500 rounded-xl shadow-lg">
                    <Zap className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-2xl">
                      Operational Stress Monitor
                    </CardTitle>
                    <p className="text-sm text-slate-600 mt-1">
                      Real-time hospital capacity and resource allocation
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {operationalStress.length === 0 ? (
                  <div className="text-center py-16 text-slate-500">
                    <Activity className="w-16 h-16 mx-auto mb-4 opacity-30 animate-pulse" />
                    <p className="text-lg">Loading operational data...</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {operationalStress.map((item, idx) => (
                      <div
                        key={idx}
                        className={`p-5 rounded-2xl border-2 shadow-lg transition-all duration-300 hover:scale-105 ${
                          item.is_stressed
                            ? "border-red-300 bg-gradient-to-br from-red-50 to-pink-50"
                            : "border-emerald-300 bg-gradient-to-br from-emerald-50 to-teal-50"
                        }`}
                      >
                        <div className="flex justify-between items-start mb-4">
                          <h3 className="font-black text-lg text-slate-900">
                            {item.region}
                          </h3>
                          {item.is_stressed ? (
                            <div className="p-2 bg-red-500 rounded-xl shadow-md animate-pulse">
                              <XCircle className="w-5 h-5 text-white" />
                            </div>
                          ) : (
                            <div className="p-2 bg-emerald-500 rounded-xl shadow-md">
                              <CheckCircle2 className="w-5 h-5 text-white" />
                            </div>
                          )}
                        </div>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between items-center">
                            <span className="text-slate-600 font-medium">
                              Capacity
                            </span>
                            <span className="font-black text-slate-900">
                              {item.avg_capacity}
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-slate-600 font-medium">
                              Occupancy
                            </span>
                            <span className="font-black text-slate-900">
                              {(item.avg_occupancy * 100).toFixed(0)}%
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-slate-600 font-medium">
                              Admissions
                            </span>
                            <span className="font-black text-slate-900">
                              {item.avg_admissions}
                            </span>
                          </div>
                          <div className="mt-3 pt-3 border-t border-white/60">
                            <span
                              className={`px-3 py-1.5 rounded-xl text-xs font-black shadow-md inline-block ${getStressColor(
                                item.stress_level
                              )}`}
                            >
                              {item.stress_level === "High"
                                ? "⚠️ HIGH STRESS"
                                : "✅ NORMAL"}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </section>

          {/* Environmental Triggers */}
          <section className="animate-slide-up" style={{ animationDelay: "0.2s" }}>
            <Card className="border-l-4 border-l-purple-500 bg-violet-50/70">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-purple-500 rounded-xl shadow-lg">
                    <Wind className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-2xl">
                      Environmental Triggers
                    </CardTitle>
                    <p className="text-sm text-slate-600 mt-1">
                      30-day air quality trends for policy decisions
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {environmentalTriggers.length === 0 ? (
                  <div className="text-center py-16 text-slate-500">
                    <Wind className="w-16 h-16 mx-auto mb-4 opacity-30 animate-pulse" />
                    <p className="text-lg">Loading environmental data...</p>
                  </div>
                ) : (
                  <div className="h-96 bg-white rounded-xl p-4">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={environmentalTriggers}>
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke="#cbd5e1"
                          strokeOpacity={0.3}
                        />
                        <XAxis
                          dataKey="date"
                          stroke="#64748b"
                          fontSize={12}
                          fontWeight={600}
                        />
                        <YAxis
                          stroke="#64748b"
                          fontSize={12}
                          fontWeight={600}
                        />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "rgba(255, 255, 255, 0.95)",
                            borderRadius: "16px",
                            border: "none",
                            boxShadow: "0 10px 40px rgba(0,0,0,0.15)",
                            padding: "12px",
                          }}
                        />
                        <Legend wrapperStyle={{ fontWeight: 600 }} />
                        <Line
                          type="monotone"
                          dataKey="pm2_5"
                          stroke="#8b5cf6"
                          strokeWidth={3}
                          name="PM2.5"
                          dot={{ fill: "#8b5cf6", r: 4 }}
                          activeDot={{ r: 6 }}
                        />
                        <Line
                          type="monotone"
                          dataKey="aqi"
                          stroke="#3b82f6"
                          strokeWidth={3}
                          name="AQI"
                          dot={{ fill: "#3b82f6", r: 4 }}
                          activeDot={{ r: 6 }}
                        />
                        <Line
                          type="monotone"
                          dataKey="no2"
                          stroke="#f59e0b"
                          strokeWidth={3}
                          name="NO2"
                          dot={{ fill: "#f59e0b", r: 4 }}
                          activeDot={{ r: 6 }}
                        />
                        <Line
                          type="monotone"
                          dataKey="o3"
                          stroke="#10b981"
                          strokeWidth={3}
                          name="O3"
                          dot={{ fill: "#10b981", r: 4 }}
                          activeDot={{ r: 6 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </CardContent>
            </Card>
          </section>

          {/* Model Validation */}
          <section className="animate-slide-up" style={{ animationDelay: "0.3s" }}>
            <Card className="border-l-4 border-l-emerald-500 bg-emerald-50/70">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-emerald-500 rounded-xl shadow-lg">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-2xl">Model Validation</CardTitle>
                    <p className="text-sm text-slate-600 mt-1">
                      Predicted vs actual admissions accuracy tracking
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {modelValidation.length === 0 ? (
                  <div className="text-center py-16 text-slate-500">
                    <TrendingUp className="w-16 h-16 mx-auto mb-4 opacity-30 animate-pulse" />
                    <p className="text-lg">Loading validation data...</p>
                  </div>
                ) : (
                  <>
                    <div className="h-96 bg-white rounded-xl p-4 mb-6">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={modelValidation}>
                          <CartesianGrid
                            strokeDasharray="3 3"
                            stroke="#cbd5e1"
                            strokeOpacity={0.3}
                          />
                          <XAxis
                            dataKey="date"
                            stroke="#64748b"
                            fontSize={12}
                            fontWeight={600}
                          />
                          <YAxis
                            stroke="#64748b"
                            fontSize={12}
                            fontWeight={600}
                          />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: "rgba(255, 255, 255, 0.95)",
                              borderRadius: "16px",
                              border: "none",
                              boxShadow: "0 10px 40px rgba(0,0,0,0.15)",
                              padding: "12px",
                            }}
                          />
                          <Legend wrapperStyle={{ fontWeight: 600 }} />
                          <Bar
                            dataKey="predicted"
                            fill="#3b82f6"
                            name="Predicted"
                            radius={[12, 12, 0, 0]}
                          />
                          <Bar
                            dataKey="actual"
                            fill="#10b981"
                            name="Actual"
                            radius={[12, 12, 0, 0]}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>

                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b-2 border-slate-200/60 bg-slate-100">
                            <th className="text-left py-3 px-4 font-bold text-slate-700">
                              Date
                            </th>
                            <th className="text-right py-3 px-4 font-bold text-slate-700">
                              Predicted
                            </th>
                            <th className="text-right py-3 px-4 font-bold text-slate-700">
                              Actual
                            </th>
                            <th className="text-right py-3 px-4 font-bold text-slate-700">
                              Error
                            </th>
                            <th className="text-right py-3 px-4 font-bold text-slate-700">
                              Accuracy
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {modelValidation.map((item, idx) => (
                            <tr
                              key={idx}
                              className="border-b border-slate-100 hover:bg-white transition-all duration-150"
                            >
                              <td className="py-3 px-4 font-semibold text-slate-900">
                                {item.date}
                              </td>
                              <td className="py-3 px-4 text-right text-blue-600 font-black">
                                {item.predicted}
                              </td>
                              <td className="py-3 px-4 text-right text-emerald-600 font-black">
                                {item.actual}
                              </td>
                              <td className="py-3 px-4 text-right text-slate-600 font-medium">
                                {item.error}
                              </td>
                              <td className="py-3 px-4 text-right">
                                <span
                                  className={`px-3 py-1.5 rounded-xl text-xs font-black shadow-md ${
                                    item.accuracy_percentage > 90
                                      ? "bg-gradient-to-r from-emerald-500 to-teal-500 text-white"
                                      : item.accuracy_percentage > 80
                                      ? "bg-gradient-to-r from-yellow-500 to-orange-500 text-white"
                                      : "bg-gradient-to-r from-red-500 to-pink-500 text-white"
                                  }`}
                                >
                                  {item.accuracy_percentage}%
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          </section>
        </div>
      </main>
    </div>
  );
};

export default AuthorityDashboard;
