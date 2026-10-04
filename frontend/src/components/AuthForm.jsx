import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function AuthForm({ mode, onSubmit, error, loading }) {
  const isLogin = mode === 'login'
const [login, setLogin] = useState('')
const [username, setUsername] = useState('')
const [email, setEmail] = useState('')
const [password, setPassword] = useState('')

    
    function handleSubmit(e) {
    e.preventDefault()

    if (isLogin) {
        onSubmit({
        login,
        password,
        })
    } else {
        onSubmit({
        username,
        email,
        password,
        })
    }
    }

    return (
    <form className="card auth-form" onSubmit={handleSubmit}>
        <h1>{isLogin ? 'Вход' : 'Регистрация'}</h1>

        {error && (
        <div className="error" role="alert">
            {error}
        </div>
        )}

        {isLogin ? (
        <label>
            Email или Username
            <input
            type="text"
            autoComplete="username"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            required
            />
        </label>
        ) : (
        <>
            <label>
            Username
            <input
                type="text"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
            />
            </label>

            <label>
            Email
            <input
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            </label>
        </>
        )}

        <label>
        Пароль
        <input
            type="password"
            autoComplete={isLogin ? 'current-password' : 'new-password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            required
        />
        </label>

        <button
        type="submit"
        className="btn-primary"
        disabled={loading}
        >
        {loading
            ? 'Подождите...'
            : isLogin
            ? 'Войти'
            : 'Создать аккаунт'}
        </button>

        <p className="hint">
        {isLogin ? (
            <>
            Нет аккаунта? <Link to="/register">Регистрация</Link>
            </>
        ) : (
            <>
            Уже есть аккаунт? <Link to="/login">Войти</Link>
            </>
        )}
        </p>
    </form>
    )
}