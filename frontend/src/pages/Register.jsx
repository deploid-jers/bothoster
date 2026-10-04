import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AuthForm from '../components/AuthForm.jsx'
import { useAuth } from '../auth/AuthProvider.jsx'
import { api } from '../api.js'


export default function Register() {
    const { refresh } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleRegister({ username, email, password }) {
    setError(null)
    setLoading(true)
    try {
        const res = await api('/v1/auth/registration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
        skipAuthRedirect: true,
        })
        const data = await res.json()
        if (!res.ok) { 
            if (res.status == 409) { setError(data.detail); return}
            setError('Не удалось зарегистрироваться'); return 
        }
        await refresh()          
        navigate('/profile')


    } catch {
      setError('Сервер недоступен')
    } finally {
      setLoading(false)
    }
  }

  return <AuthForm mode="register" onSubmit={handleRegister} error={error} loading={loading} />
}