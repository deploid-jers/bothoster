import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from './AuthProvider.jsx'


export default function GuestRoute() {
  const { status } = useAuth()
  if (status === 'loading') return <p>Загрузка...</p>
  if (status === 'authed') return <Navigate to="/profile" replace />
  return <Outlet />
}