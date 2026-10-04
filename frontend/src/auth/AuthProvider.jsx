import { createContext, useContext, useEffect, useState } from 'react'
import { api, setUnauthorizedHandler } from '../api'

const AuthContext = createContext(null)
export const useAuth = () => useContext(AuthContext)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [status, setStatus] = useState('loading') // loading | authed | anon

  function reset() { setUser(null); setStatus('anon') }

  async function refresh() {
    try {
      const res = await api('/v1/auth/me', { skipAuthRedirect: true })
      if (res.ok) { setUser(await res.json()); setStatus('authed') }
      else reset()
    } catch { reset() }
  }

  async function logout() {
    await api('/v1/auth/logout', { method: 'POST', skipAuthRedirect: true })
    reset()
  }

  useEffect(() => {
    setUnauthorizedHandler(reset)
    refresh()
  }, [])

  return (
    <AuthContext.Provider value={{ user, status, refresh, logout }}>
      {children}
    </AuthContext.Provider>
  )
}