import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import CitizenDashboard from './pages/CitizenDashboard';
import AuthorityDashboard from './pages/AuthorityDashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/citizen" element={<CitizenDashboard />} />
          <Route path="/authority" element={<AuthorityDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
