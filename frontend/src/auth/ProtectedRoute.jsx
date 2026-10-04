import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from './AuthProvider.jsx'

export default function ProtectedRoute() {
  const { status } = useAuth()
  if (status === 'loading') return <p>Загрузка...</p>
  if (status === 'anon') return <Navigate to="/login" replace />
  return <Outlet />
}