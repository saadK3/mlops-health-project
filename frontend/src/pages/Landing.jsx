import React from 'react';
import { Link } from 'react-router-dom';
import { 
  User, 
  ShieldAlert, 
  Activity, 
  TrendingUp, 
  Zap, 
  BarChart3,
  Heart,
  Wind,
  ArrowRight,
  CheckCircle2,
  Sparkles
} from 'lucide-react';

const Landing = () => {
  const features = [
    {
      icon: <Activity className="w-6 h-6" />,
      title: "Real-time Monitoring",
      description: "Track health metrics and environmental factors in real-time"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Predictive Analytics",
      description: "AI-powered predictions for hospital admissions and health risks"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Data Visualization",
      description: "Comprehensive dashboards with interactive charts and insights"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Instant Alerts",
      description: "Get notified about critical health conditions and environmental risks"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-cyan-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Hero Section */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-20">
        <div className="max-w-6xl mx-auto w-full">
          {/* Main Hero Content */}
          <div className="text-center mb-16 animate-fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full text-sm font-semibold text-indigo-600 mb-6 shadow-lg">
              <Sparkles className="w-4 h-4" />
              Powered by Advanced MLOps
            </div>
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-black mb-6 tracking-tight">
              <span className="bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-600 bg-clip-text text-transparent">
                HealthGuard
              </span>
              <span className="block text-slate-800 mt-2">AI Platform</span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              Advanced health monitoring and risk assessment powered by machine learning.
              <span className="block mt-2 text-lg text-slate-500">
                Protect communities with predictive analytics and real-time insights.
              </span>
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <Link
                to="/citizen"
                className="group px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-2xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 flex items-center gap-2"
              >
                <User className="w-5 h-5" />
                Citizen Portal
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/authority"
                className="group px-8 py-4 bg-white text-indigo-600 rounded-2xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 flex items-center gap-2 border-2 border-indigo-200"
              >
                <ShieldAlert className="w-5 h-5" />
                Authority Dashboard
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-white/50"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-bold text-slate-800 mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>

          {/* Dashboard Cards */}
          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            <Link
              to="/citizen"
              className="group relative bg-white/90 backdrop-blur-sm p-8 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:-translate-y-2 border border-blue-100 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative z-10">
                <div className="flex items-center gap-4 mb-6">
                  <div className="p-4 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <User className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-black text-slate-800 mb-1">Citizen Portal</h2>
                    <p className="text-blue-600 font-semibold">Personal Health Dashboard</p>
                  </div>
                </div>
                <p className="text-slate-600 mb-6 leading-relaxed">
                  Monitor your personal health risk, view historical trends, and receive personalized alerts based on your location and health metrics.
                </p>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 text-sm text-slate-700">
                    <CheckCircle2 className="w-5 h-5 text-blue-500" />
                    <span>Real-time health risk assessment</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-slate-700">
                    <CheckCircle2 className="w-5 h-5 text-blue-500" />
                    <span>Environmental factor tracking</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-slate-700">
                    <CheckCircle2 className="w-5 h-5 text-blue-500" />
                    <span>Personalized recommendations</span>
                  </div>
                </div>
                <div className="mt-6 flex items-center text-blue-600 font-bold group-hover:gap-3 transition-all">
                  <span>Explore Dashboard</span>
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-2 transition-transform" />
                </div>
              </div>
            </Link>

            <Link
              to="/authority"
              className="group relative bg-white/90 backdrop-blur-sm p-8 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:-translate-y-2 border border-indigo-100 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative z-10">
                <div className="flex items-center gap-4 mb-6">
                  <div className="p-4 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <ShieldAlert className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-black text-slate-800 mb-1">Authority Dashboard</h2>
                    <p className="text-indigo-600 font-semibold">Command Center</p>
                  </div>
                </div>
                <p className="text-slate-600 mb-6 leading-relaxed">
                  Monitor regional health risks, analyze spatial data, track operational stress, and manage public health alerts with comprehensive analytics.
                </p>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 text-sm text-slate-700">
                    <CheckCircle2 className="w-5 h-5 text-indigo-500" />
                    <span>Spatial risk analysis</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-slate-700">
                    <CheckCircle2 className="w-5 h-5 text-indigo-500" />
                    <span>Operational stress monitoring</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-slate-700">
                    <CheckCircle2 className="w-5 h-5 text-indigo-500" />
                    <span>Model validation & accuracy</span>
                  </div>
                </div>
                <div className="mt-6 flex items-center text-indigo-600 font-bold group-hover:gap-3 transition-all">
                  <span>Access Dashboard</span>
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-2 transition-transform" />
                </div>
              </div>
            </Link>
          </div>

          {/* Stats Section */}
          <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg">
              <div className="text-4xl font-black bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent mb-2">24/7</div>
              <div className="text-sm text-slate-600 font-semibold">Real-time Monitoring</div>
            </div>
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg">
              <div className="text-4xl font-black bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">AI</div>
              <div className="text-sm text-slate-600 font-semibold">Powered Predictions</div>
            </div>
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg">
              <div className="text-4xl font-black bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-2">99%</div>
              <div className="text-sm text-slate-600 font-semibold">Accuracy Rate</div>
            </div>
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg">
              <div className="text-4xl font-black bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-2">100+</div>
              <div className="text-sm text-slate-600 font-semibold">Data Points</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
