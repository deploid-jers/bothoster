import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import Profile from './pages/Profile.jsx'
import NotFound from './pages/NotFound.jsx'
import GuestRoute from './auth/GuestRoute.jsx'

import ProtectedRoute from './auth/ProtectedRoute.jsx'

export default function App() {
  return (
    <>
      <Navbar />
      <main className="container">
        <Routes>

          <Route path="/" element={<Home />} />

          <Route element={<GuestRoute />}>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Route>

          <Route element={<ProtectedRoute />}>
            <Route path="/profile" element={<Profile />} />
          </Route> 

          <Route path="*" element={<NotFound />} />

        </Routes>
      </main>
    </>
  )
}