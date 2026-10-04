import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AuthForm from '../components/AuthForm.jsx'
import { useAuth } from '../auth/AuthProvider.jsx'
import { api } from '../api.js'

export default function Login() {
    const { refresh } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleLogin({ login, password }) {
    setError(null)
    setLoading(true)
    try {
        console.log(JSON.stringify({ login, password }))
        const res = await api('/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password }),
        skipAuthRedirect: true,
        })
        if (!res.ok) { setError('Неверный email или пароль'); return }
        await refresh()          
        navigate('/profile')
    } catch  {
      setError('Сервер недоступен')
    } finally {
      setLoading(false)
    }
  }

  return <AuthForm mode="login" onSubmit={handleLogin} error={error} loading={loading} />
}