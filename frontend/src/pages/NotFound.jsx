import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <section className="hero">
      <h1>404</h1>
      <p>Такой страницы нет.</p>
      <Link to="/" className="btn-primary">На главную</Link>
    </section>
  )
}