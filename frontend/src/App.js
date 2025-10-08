import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { FileUpload } from './pages/FileUpload';
import { YieldComparisonReport } from './pages/reports/YieldComparisonReport';
import { FieldEfficiencyReport } from './pages/reports/FieldEfficiencyReport';
import { VarietyPerformanceReport } from './pages/reports/VarietyPerformanceReport';
import { UserManagement } from './pages/UserManagement';
import { UploadHistory } from './pages/UploadHistory';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              } 
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="upload" element={<FileUpload />} />
              <Route path="reports">
                <Route path="yield-comparison" element={<YieldComparisonReport />} />
                <Route path="field-efficiency" element={<FieldEfficiencyReport />} />
                <Route path="variety-performance" element={<VarietyPerformanceReport />} />
              </Route>
              <Route path="upload-history" element={<UploadHistory />} />
              <Route path="users" element={<UserManagement />} />
            </Route>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;


