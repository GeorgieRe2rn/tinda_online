import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import { getCountries, getCampusMoment } from '../api/client'

export function Dashboard() {
  const { user, signOut } = useAuth()
  const [campusMoment, setCampusMoment] = useState(null)
  const [momentError, setMomentError] = useState('')
  const [countries, setCountries] = useState(null)
  const [soapError, setSoapError] = useState('')

  useEffect(() => {
    getCampusMoment().then(setCampusMoment).catch(err => setMomentError(err.message))
    getCountries().then(setCountries).catch(err => setSoapError(err.message))
  }, [])

  const displayName = user?.first_name || user?.username || user?.email?.split('@')[0] || 'Estudiante'
  return <div className="dashboard-shell">
    <aside className="sidebar"><a className="brand" href="/dashboard"><span className="brand-mark">t.</span><span>TUNTO<span className="brand-muted"> ONLINE</span></span></a>
      <div className="side-label">ESPACIO PERSONAL</div><nav className="side-nav"><a className="side-link active" href="/dashboard"><span>◫</span> Resumen</a><a className="side-link" href="/swagger/" target="_blank" rel="noreferrer"><span>⌘</span> API Docs</a></nav>
      <div className="sidebar-bottom"><div className="avatar">{displayName.slice(0, 1).toUpperCase()}</div><div className="profile-mini"><strong>{displayName}</strong><span>Miembro del campus</span></div><button className="icon-button" title="Cerrar sesión" onClick={signOut}>↗</button></div>
    </aside>
    <main className="dashboard-main"><header className="topbar"><span>MI ESPACIO <span className="slash">/</span> RESUMEN</span><div className="topbar-user"><span className="online-dot"></span> SESIÓN ACTIVA</div></header>
      <section className="welcome-block"><div><span className="eyebrow">TU CAMPUS, TU COMUNIDAD</span><h1>Hola, {displayName}<span className="sun"> ✳</span></h1><p>Un buen día empieza con grandes conexiones.</p></div><div className="date-chip">TUNTO ONLINE <span>✳</span></div></section>
      <section className="hero-card"><div className="hero-text"><span className="eyebrow">CAMPUS MARKETPLACE · EST. 2026</span><h2>Haz que cada día<br />cuente.</h2><p>Descubre algo nuevo. Comparte lo que tienes.<br />Encuentra tu lugar en el campus.</p><a className="button button-light" href="#inspiracion">Explorar mi espacio <span>↘</span></a></div><div className="hero-art" aria-hidden="true"><div className="art-sun"></div><div className="art-arch"><div className="arch-inner"></div></div><div className="art-spark spark-one">✳</div><div className="art-spark spark-two">✳</div><div className="art-caption">A LITTLE MORE<br />CAMPUS MAGIC</div></div><span className="hero-index">01 — 03</span></section>
      <div className="section-heading" id="inspiracion"><div><span className="eyebrow">UN POCO DE INSPIRACIÓN</span><h2>Tu dosis de buena energía.</h2></div><span className="source-tag"><i></i> CONTENIDO EN VIVO</span></div>
      <section className="widget-grid"><article className="quote-card"><div className="widget-top"><span className="widget-kicker"><span>✳</span> PAUSA DE CAMPUS</span><span className="api-pill"><i></i> API EXTERNA</span></div>{campusMoment?.status === 'success' ? <><div className="campus-image-frame"><img className="campus-image" src={campusMoment.message} alt="Compañero de campus del día, imagen aleatoria de Dog CEO" /></div><div className="quote-bottom"><span>Un compañero para alegrar el día.</span><span>DOG CEO API</span></div></> : momentError ? <p className="widget-error">{momentError}</p> : <p className="widget-loading">Buscando a nuestro compañero de campus…</p>}</article>
        <article className="soap-card"><div className="widget-top"><span className="widget-kicker"><span>⌘</span> ALREDEDOR DEL MUNDO</span><span className="soap-pill"><i></i> SERVICIO SOAP</span></div><h3>Un campus,<br />muchos lugares.</h3>{countries ? <div className="soap-result"><div className="country-count">{countries.count}<span> países</span></div><span>Catálogo consultado desde Django + Zeep</span></div> : soapError ? <p className="widget-error">{soapError}</p> : <p className="widget-loading">Consultando servicio SOAP…</p>}<span className="soap-watermark">◎</span></article></section>
      <footer className="dashboard-footer"><span>TUNTO ONLINE <span className="footer-dot">✳</span> TU VIDA EN CAMPUS, A TU MANERA.</span><span>PERFIL · {user?.email}</span></footer>
    </main>
  </div>
}
