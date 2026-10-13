import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../api.js'
import { useAuth } from '../auth/AuthProvider.jsx'

export default function VerifyEmail() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const { status, refresh } = useAuth()

  const token = useRef(params.get('token'))  
  const started = useRef(false)               
  const [state, setState] = useState(token.current ? 'loading' : 'invalid')

  useEffect(() => {
    if (!token.current || started.current) return
    started.current = true

    navigate('/verify', { replace: true })  

    async function confirm() {
      try {
        const res = await api('/v1/user/email/confirm', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token: token.current }),
          skipAuthRedirect: true,
        })
        console.log(res)
        if (res.ok) {
          setState('success')
          await refresh()                     
        } else {
          setState('invalid')
        }
      } catch {
        setState('network')
      }
    }
    confirm()
  }, [])

  return (
    <div className="card center">
      {state === 'loading' && <p>Подтверждаем почту...</p>}

      {state === 'success' && (
        <>
          <div className="status-icon ok">✓</div>
          <h1>Почта подтверждена</h1>
          <Link className="btn-primary" to={status === 'authed' ? '/profile' : '/login'}>
            {status === 'authed' ? 'В профиль' : 'Войти'}
          </Link>
        </>
      )}

      {state === 'invalid' && (
        <>
          <div className="status-icon fail">!</div>
          <h1>Ссылка недействительна</h1>
          <p className="hint">Она могла устареть или уже быть использована.</p>
          <Link className="btn-secondary" to="/profile">В профиль</Link>
          {/* TODO: кнопка «Отправить письмо ещё раз» -> POST /email/resend */}
        </>
      )}

      {state === 'network' && (
        <>
          <h1>Сервер недоступен</h1>
          <p className="hint">Обновите страницу позже. Ссылка могла не сгореть, но проверить нельзя: токен из адреса уже убран.</p>
        </>
      )}
    </div>
  )
}