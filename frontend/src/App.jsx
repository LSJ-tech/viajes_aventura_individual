import { useEffect, useState } from 'react'
import './App.css'
import Admin from './Admin'
import Clientes from './Clientes'
import Destinos from './Destinos'
import { IconCalendarCheck, IconMapPin, IconPackage } from './icons'
import Paquetes from './Paquetes'
import Reservas from './Reservas'

const TOKEN_KEY = 'viajes_aventura_token'
const ADMIN_TOKEN_KEY = 'viajes_aventura_admin_token'

// Un JWT es siempre header.payload.firma en base64url; valida esa forma antes de
// persistir cualquier valor en localStorage (evita guardar datos no confiables
// si la respuesta del backend llegara alterada o incompleta).
const FORMATO_JWT = /^[\w-]+\.[\w-]+\.[\w-]+$/

function guardarToken(clave, valor) {
  if (typeof valor === 'string' && FORMATO_JWT.test(valor)) {
    localStorage.setItem(clave, valor)
  }
}

const TABS = [
  { id: 'destinos', label: 'Destinos', Icon: IconMapPin },
  { id: 'paquetes', label: 'Paquetes', Icon: IconPackage },
  { id: 'reservas', label: 'Reservas', Icon: IconCalendarCheck },
]

function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [perfil, setPerfil] = useState(null)
  const [adminToken, setAdminToken] = useState(() => localStorage.getItem(ADMIN_TOKEN_KEY) || '')
  const [tab, setTab] = useState('destinos')

  useEffect(() => {
    if (!token) {
      setPerfil(null)
      return
    }
    fetch('/api/clientes/me', { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => {
        if (!res.ok) throw new Error()
        return res.json()
      })
      .then(setPerfil)
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY)
        setToken('')
      })
  }, [token])

  const iniciarSesion = (data) => {
    guardarToken(TOKEN_KEY, data.access_token)
    setToken(data.access_token)
    setPerfil(data.cliente)
  }

  const cerrarSesion = () => {
    localStorage.removeItem(TOKEN_KEY)
    setToken('')
    setPerfil(null)
  }

  const iniciarSesionAdmin = (accessToken) => {
    guardarToken(ADMIN_TOKEN_KEY, accessToken)
    setAdminToken(accessToken)
  }

  const cerrarSesionAdmin = () => {
    localStorage.removeItem(ADMIN_TOKEN_KEY)
    setAdminToken('')
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            ⛰
          </span>
          <div>
            <h1>Viajes Aventura</h1>
            <p className="subtitulo">Sistema de gestión de agencia de viajes — TI3V21, INACAP Valparaíso</p>
          </div>
        </div>
        <div className="auth-chips">
          <Admin adminToken={adminToken} onSesionIniciada={iniciarSesionAdmin} onCerrarSesion={cerrarSesionAdmin} />
          <Clientes perfil={perfil} onSesionIniciada={iniciarSesion} onCerrarSesion={cerrarSesion} />
        </div>
      </header>

      <nav className="tabs-nav">
        {TABS.map(({ id, label, Icon }) => (
          <button key={id} className={tab === id ? 'tab-activo' : ''} onClick={() => setTab(id)}>
            <Icon />
            {label}
          </button>
        ))}
      </nav>

      <main className="content">
        {tab === 'destinos' && <Destinos adminToken={adminToken} />}
        {tab === 'paquetes' && <Paquetes adminToken={adminToken} />}
        {tab === 'reservas' && <Reservas token={token} perfil={perfil} />}
      </main>
    </div>
  )
}

export default App
