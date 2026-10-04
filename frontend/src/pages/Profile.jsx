import { useAuth } from '../auth/AuthProvider.jsx'



export default function Profile() {
    const { user, logout } = useAuth()
  return (
    <div className="card">
      <h1>Профиль</h1>
        <p>Email: {user.email}</p>
        <button className="btn-secondary" onClick={logout}>Выйти</button>
    </div>
  )
}