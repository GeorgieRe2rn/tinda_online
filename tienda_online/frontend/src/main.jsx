import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { Dashboard } from './pages/Dashboard'
import './styles.css'

function ProtectedRoute({ children }) {
  const { token, loading } = useAuth()
  if (loading) return <div className="loading-screen">Cargando tu espacio…</div>
  return token ? children : <Navigate to="/login" replace />
}

function App() {
  return <AuthProvider><BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}><Routes>
    <Route path="/" element={<Navigate to="/dashboard" replace />} />
    <Route path="/login" element={<Login />} />
    <Route path="/registro" element={<Register />} />
    <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes></BrowserRouter></AuthProvider>
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>)
