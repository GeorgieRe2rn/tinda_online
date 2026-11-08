import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../auth/AuthContext'

export function Login() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(event) {
    event.preventDefault(); setError(''); setBusy(true)
    try {
      const access = await signIn({ email, password })
      console.info('[Tunto Online] Access token recibido:', access)
      navigate('/dashboard')
    } catch (err) { setError(err.message) } finally { setBusy(false) }
  }

  return (
    <main className="auth-shell">
      <section className="auth-copy">
        <Link className="brand brand-light" to="/login"><span className="brand-mark">t.</span><span>TUNTO<span className="brand-muted"> ONLINE</span></span></Link>
        <div className="auth-message"><span className="eyebrow">CAMPUS MARKETPLACE</span><h1>Todo lo que necesitas para tu vida en campus.</h1><p>Una comunidad universitaria para descubrir, compartir y conectar.</p><div className="auth-orbit"><span>✳</span><span>conecta · comparte · descubre</span></div></div>
        <span className="auth-foot">UNIVERSITY GOODS, GOOD ENERGY.</span>
      </section>
      <section className="auth-panel">
        <div className="auth-card"><span className="eyebrow">QUÉ BUENO VERTE</span><h2>Inicia sesión</h2><p className="muted">Accede a tu espacio de Tunto Online.</p>
          <form onSubmit={submit} className="form-stack">
            <label>Correo electrónico<input autoComplete="email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="tu@universidad.edu" required /></label>
            <label>Contraseña<input autoComplete="current-password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Tu contraseña" required /></label>
            {error && <div className="error-box" role="alert">{error}</div>}
            <button className="button button-dark button-full" disabled={busy}>{busy ? 'Entrando…' : 'Entrar a mi cuenta'} <span>↗</span></button>
          </form>
          <p className="auth-switch">¿Aún no tienes cuenta? <Link to="/registro">Crear cuenta</Link></p>
        </div>
        <span className="panel-note">HECHO PARA TU DÍA A DÍA EN CAMPUS <span>✳</span></span>
      </section>
    </main>
  )
}
