import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar
} from 'recharts';
import { 
  Activity, 
  Wind, 
  Thermometer, 
  Heart, 
  AlertCircle, 
  CheckCircle,
  Home,
  Droplets,
  Gauge,
  TrendingUp,
  Zap,
  Shield,
  ArrowLeft,
  RefreshCw
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import Navbar from '../components/Navbar';

const CitizenDashboard = () => {
  const [formData, setFormData] = useState({
    aqi: 45,
    pm2_5: 12,
    pm10: 20,
    no2: 15,
    o3: 30,
    temperature: 25,
    humidity: 60,
    hospital_capacity: 80,
    occupancy_ratio: 0.7,
    population_density: "Urban",
    heart_rate: 72,
    oxygen_saturation: 98,
    steps: 8000,
    sleep_hours: 7,
    respiratory_rate: 16,
    body_temp: 36.6,
    user_id: "user_123",
    region: "Downtown"
  });

  const [prediction, setPrediction] = useState(null);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  // Generate mock trends data if API doesn't exist
  useEffect(() => {
    const generateMockTrends = () => {
      const mockData = [];
      const now = new Date();
      for (let i = 6; i >= 0; i--) {
        const date = new Date(now);
        date.setHours(date.getHours() - i);
        mockData.push({
          time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          risk_score: 5 + Math.random() * 5,
          timestamp: date.toISOString()
        });
      }
      setTrends(mockData);
    };
    generateMockTrends();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'population_density' || name === 'user_id' || name === 'region' ? value : Number(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      console.log('Sending prediction request with data:', formData);
      const response = await axios.post('http://localhost:5000/predict', formData);
      console.log('Prediction response:', response.data);
      setPrediction(response.data.predicted_hospital_admissions);
      setLastUpdated(new Date());
      // Add to trends
      const newTrend = {
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        risk_score: response.data.predicted_hospital_admissions,
        timestamp: new Date().toISOString()
      };
      setTrends(prev => [...prev.slice(-6), newTrend]);
    } catch (err) {
      console.error('Full error object:', err);
      console.error('Error response:', err.response);
      
      // Show the actual error message from the backend
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Backend Error: ${err.response.data.error}`);
      } else if (err.response) {
        setError(`HTTP Error ${err.response.status}: ${err.response.statusText}`);
      } else if (err.request) {
        setError('Network Error: Could not reach backend. Is the server running on port 5000?');
      } else {
        setError(`Error: ${err.message || 'Failed to get prediction'}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevel = (value) => {
    if (value === null) return { 
      level: 'Unknown', 
      borderColor: 'border-slate-400',
      bgGradient: 'from-slate-50 to-white',
      circleBg: 'bg-slate-100',
      textColor: 'text-slate-600',
      badgeBg: 'bg-slate-500'
    };
    if (value > 15) return { 
      level: 'Critical', 
      borderColor: 'border-red-500',
      bgGradient: 'from-red-50 to-white',
      circleBg: 'bg-red-100',
      textColor: 'text-red-600',
      badgeBg: 'bg-red-500'
    };
    if (value > 10) return { 
      level: 'High', 
      borderColor: 'border-orange-500',
      bgGradient: 'from-orange-50 to-white',
      circleBg: 'bg-orange-100',
      textColor: 'text-orange-600',
      badgeBg: 'bg-orange-500'
    };
    if (value > 5) return { 
      level: 'Moderate', 
      borderColor: 'border-yellow-500',
      bgGradient: 'from-yellow-50 to-white',
      circleBg: 'bg-yellow-100',
      textColor: 'text-yellow-600',
      badgeBg: 'bg-yellow-500'
    };
    return { 
      level: 'Low', 
      borderColor: 'border-green-500',
      bgGradient: 'from-green-50 to-white',
      circleBg: 'bg-green-100',
      textColor: 'text-green-600',
      badgeBg: 'bg-green-500'
    };
  };

  const riskInfo = getRiskLevel(prediction);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-10">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <div className="flex items-center gap-3 mb-4">
            <Link 
              to="/" 
              className="p-2 hover:bg-white/50 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-slate-600" />
            </Link>
            <div>
              <h1 className="text-4xl md:text-5xl font-black gradient-text mb-2">
                Citizen Health Portal
              </h1>
              <p className="text-slate-600 text-lg">
                Monitor your personal health risk and environmental factors
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Input Form & Charts */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white border-0">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-blue-100 text-xs font-medium mb-1">Heart Rate</p>
                      <p className="text-2xl font-black">{formData.heart_rate} bpm</p>
                    </div>
                    <Heart className="w-8 h-8 opacity-40" />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-purple-500 to-pink-500 text-white border-0">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-purple-100 text-xs font-medium mb-1">Body Temp</p>
                      <p className="text-2xl font-black">{formData.body_temp}°C</p>
                    </div>
                    <Thermometer className="w-8 h-8 opacity-40" />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-emerald-500 to-teal-500 text-white border-0">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-emerald-100 text-xs font-medium mb-1">O2 Saturation</p>
                      <p className="text-2xl font-black">{formData.oxygen_saturation}%</p>
                    </div>
                    <Activity className="w-8 h-8 opacity-40" />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-orange-500 to-red-500 text-white border-0">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-orange-100 text-xs font-medium mb-1">AQI</p>
                      <p className="text-2xl font-black">{formData.aqi}</p>
                    </div>
                    <Wind className="w-8 h-8 opacity-40" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Input Form */}
            <Card className="border-l-4 border-l-blue-500">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-blue-500 rounded-xl shadow-lg">
                    <Activity className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-2xl">Health & Environment Input</CardTitle>
                    <p className="text-sm text-slate-600 mt-1">Enter your current health and environmental metrics</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Health Metrics */}
                    <div className="space-y-4">
                      <h3 className="font-bold text-slate-800 flex items-center gap-2">
                        <Heart className="w-4 h-4 text-red-500" />
                        Health Metrics
                      </h3>
                      <div className="space-y-3">
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Heart Rate (bpm)</label>
                          <input 
                            type="number" 
                            name="heart_rate" 
                            value={formData.heart_rate} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Body Temperature (°C)</label>
                          <input 
                            type="number" 
                            step="0.1"
                            name="body_temp" 
                            value={formData.body_temp} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Oxygen Saturation (%)</label>
                          <input 
                            type="number" 
                            name="oxygen_saturation" 
                            value={formData.oxygen_saturation} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Respiratory Rate</label>
                          <input 
                            type="number" 
                            name="respiratory_rate" 
                            value={formData.respiratory_rate} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                      </div>
                    </div>

                    {/* Environmental Metrics */}
                    <div className="space-y-4">
                      <h3 className="font-bold text-slate-800 flex items-center gap-2">
                        <Wind className="w-4 h-4 text-blue-500" />
                        Environmental Factors
                      </h3>
                      <div className="space-y-3">
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Air Quality Index (AQI)</label>
                          <input 
                            type="number" 
                            name="aqi" 
                            value={formData.aqi} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">PM2.5 (μg/m³)</label>
                          <input 
                            type="number" 
                            name="pm2_5" 
                            value={formData.pm2_5} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Temperature (°C)</label>
                          <input 
                            type="number" 
                            name="temperature" 
                            value={formData.temperature} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Population Density</label>
                          <select 
                            name="population_density" 
                            value={formData.population_density} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          >
                            <option value="Urban">Urban</option>
                            <option value="Suburban">Suburban</option>
                            <option value="Rural">Rural</option>
                          </select>
                        </div>
                        <div>
                          <label className="text-sm font-medium text-slate-700 mb-1 block">Region</label>
                          <select 
                            name="region" 
                            value={formData.region} 
                            onChange={handleChange}
                            className="w-full p-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                          >
                            <option value="Downtown">Downtown</option>
                            <option value="Suburbs">Suburbs</option>
                            <option value="Industrial">Industrial</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>

                  {error && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <>
                        <RefreshCw className="w-5 h-5 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Zap className="w-5 h-5" />
                        Analyze Health Risk
                      </>
                    )}
                  </button>
                </form>
              </CardContent>
            </Card>

            {/* Trends Chart */}
            <Card className="border-l-4 border-l-purple-500">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-purple-500 rounded-xl shadow-lg">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-2xl">Risk Trends</CardTitle>
                    <p className="text-sm text-slate-600 mt-1">Historical risk score over time</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={trends}>
                      <defs>
                        <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis 
                        dataKey="time" 
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
                      <Area
                        type="monotone"
                        dataKey="risk_score"
                        stroke="#6366f1"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorRisk)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column: Results & Alerts */}
          <div className="space-y-6">
            {/* Risk Score Card */}
            {prediction !== null ? (
              <Card className={`border-l-4 ${riskInfo.borderColor} bg-gradient-to-br ${riskInfo.bgGradient}`}>
                <CardContent className="flex flex-col items-center text-center py-8">
                  <div className={`w-32 h-32 rounded-full ${riskInfo.circleBg} flex items-center justify-center mb-6 shadow-lg`}>
                    <span className={`text-5xl font-black ${riskInfo.textColor}`}>{prediction.toFixed(1)}</span>
                  </div>
                  <h3 className="text-2xl font-black text-slate-800 mb-2">Risk Score</h3>
                  <p className="text-slate-600 text-sm mb-4">
                    Predicted hospital admissions
                  </p>
                  <div className={`px-6 py-3 rounded-full text-sm font-black shadow-md ${riskInfo.badgeBg} text-white`}>
                    {riskInfo.level} RISK
                  </div>
                  <p className="text-xs text-slate-500 mt-4">
                    Last updated: {lastUpdated.toLocaleTimeString()}
                  </p>
                </CardContent>
              </Card>
            ) : (
              <Card className="border-l-4 border-l-slate-400">
                <CardContent className="flex flex-col items-center text-center py-12">
                  <div className="w-24 h-24 rounded-full bg-slate-100 flex items-center justify-center mb-6">
                    <Shield className="w-12 h-12 text-slate-400" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-600 mb-2">No Analysis Yet</h3>
                  <p className="text-slate-500 text-sm">
                    Submit your health metrics to get a risk assessment
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Active Alerts */}
            <Card className="border-l-4 border-l-orange-500">
              <CardHeader gradient>
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-500 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-white" />
                  </div>
                  <CardTitle>Active Alerts</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-start gap-3 p-4 bg-orange-50 rounded-xl border border-orange-200">
                    <Thermometer className="w-5 h-5 text-orange-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <h4 className="font-bold text-orange-900 mb-1">Temperature Alert</h4>
                      <p className="text-sm text-orange-700">Current temperature: {formData.temperature}°C</p>
                      {formData.temperature > 30 && (
                        <p className="text-xs text-orange-600 mt-1">⚠️ High temperature detected</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-xl border border-blue-200">
                    <Wind className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <h4 className="font-bold text-blue-900 mb-1">Air Quality</h4>
                      <p className="text-sm text-blue-700">
                        AQI: {formData.aqi} - {formData.aqi < 50 ? 'Good' : formData.aqi < 100 ? 'Moderate' : 'Unhealthy'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 p-4 bg-emerald-50 rounded-xl border border-emerald-200">
                    <CheckCircle className="w-5 h-5 text-emerald-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <h4 className="font-bold text-emerald-900 mb-1">Health Status</h4>
                      <p className="text-sm text-emerald-700">All vital signs within normal range</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Health Metrics Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-600">Steps Today</span>
                    <span className="font-bold text-slate-800">{formData.steps.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-600">Sleep Hours</span>
                    <span className="font-bold text-slate-800">{formData.sleep_hours}h</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-600">Humidity</span>
                    <span className="font-bold text-slate-800">{formData.humidity}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default CitizenDashboard;
