import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { register } from '../api/client'

export function Register() {
  const navigate = useNavigate()
  const [values, setValues] = useState({ username: '', email: '', first_name: '', last_name: '', phone: '', password: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  function change(event) { setValues({ ...values, [event.target.name]: event.target.value }) }
  async function submit(event) {
    event.preventDefault(); setError(''); setBusy(true)
    try { await register(values); navigate('/login', { state: { registered: true } }) }
    catch (err) { setError(err.message) } finally { setBusy(false) }
  }
  return <main className="auth-shell">
    <section className="auth-copy"><Link className="brand brand-light" to="/login"><span className="brand-mark">t.</span><span>TUNTO<span className="brand-muted"> ONLINE</span></span></Link><div className="auth-message"><span className="eyebrow">TU VIDA EN CAMPUS</span><h1>Un gran campus empieza con buenas conexiones.</h1><p>Encuentra personas y cosas que hacen tu día más fácil.</p></div><span className="auth-foot">UNIVERSITY GOODS, GOOD ENERGY.</span></section>
    <section className="auth-panel"><div className="auth-card"><span className="eyebrow">ÚNETE A LA COMUNIDAD</span><h2>Crea tu cuenta</h2><p className="muted">Completa tus datos para comenzar.</p>
      <form onSubmit={submit} className="form-stack"><div className="form-row"><label>Nombre de usuario<input name="username" value={values.username} onChange={change} required /></label><label>Teléfono<input name="phone" value={values.phone} onChange={change} /></label></div>
        <div className="form-row"><label>Nombre<input name="first_name" value={values.first_name} onChange={change} /></label><label>Apellido<input name="last_name" value={values.last_name} onChange={change} /></label></div>
        <label>Correo electrónico<input name="email" type="email" autoComplete="email" value={values.email} onChange={change} required /></label>
        <label>Contraseña<input name="password" type="password" autoComplete="new-password" value={values.password} onChange={change} minLength={8} required /><small>Mínimo 8 caracteres</small></label>
        {error && <div className="error-box" role="alert">{error}</div>}<button className="button button-dark button-full" disabled={busy}>{busy ? 'Creando cuenta…' : 'Crear mi cuenta'} <span>↗</span></button>
      </form><p className="auth-switch">¿Ya tienes una cuenta? <Link to="/login">Iniciar sesión</Link></p>
    </div><span className="panel-note">HECHO PARA TU DÍA A DÍA EN CAMPUS <span>✳</span></span></section>
  </main>
}
