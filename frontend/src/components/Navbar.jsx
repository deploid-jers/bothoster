import { NavLink } from 'react-router-dom'
import { useAuth } from '../auth/AuthProvider.jsx'


export default function Navbar() {
    const { status } = useAuth()
    if (status === 'authed') {
        return (
            <nav className="navbar">
                <NavLink to="/" className="brand">MyApp</NavLink>
                <div className="nav-links">
                    <NavLink to="/profile">Профиль</NavLink>
                </div>
            </nav>
        )
    }
    else {
        return (
            <nav className="navbar">
                <NavLink to="/" className="brand">MyApp</NavLink>
                <div className="nav-links">
                    <NavLink to="/login">Войти</NavLink>
                    <NavLink to="/register" className="btn-primary">Регистрация</NavLink>
                </div>
            </nav>
        )
    }

}