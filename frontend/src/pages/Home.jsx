import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <section className="hero">
      <h1>Добро пожаловать в MyApp</h1>
      <p>Короткое описание проекта в одну-две строки.</p>
      <div className="hero-actions">
        <Link to="/register" className="btn-primary">Начать</Link>
        <Link to="/login" className="btn-secondary">Войти</Link>
      </div>
    </section>
  )
}