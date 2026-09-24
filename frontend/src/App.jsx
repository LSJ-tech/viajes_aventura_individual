import { useEffect, useState } from 'react'
import './App.css'
import Admin from './Admin'
import Clientes from './Clientes'
import Destinos from './Destinos'
import Paquetes from './Paquetes'
import Reservas from './Reservas'

const TOKEN_KEY = 'viajes_aventura_token'
const ADMIN_TOKEN_KEY = 'viajes_aventura_admin_token'

function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [perfil, setPerfil] = useState(null)
  const [adminToken, setAdminToken] = useState(() => localStorage.getItem(ADMIN_TOKEN_KEY) || '')

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
    localStorage.setItem(TOKEN_KEY, data.access_token)
    setToken(data.access_token)
    setPerfil(data.cliente)
  }

  const cerrarSesion = () => {
    localStorage.removeItem(TOKEN_KEY)
    setToken('')
    setPerfil(null)
  }

  const iniciarSesionAdmin = (accessToken) => {
    localStorage.setItem(ADMIN_TOKEN_KEY, accessToken)
    setAdminToken(accessToken)
  }

  const cerrarSesionAdmin = () => {
    localStorage.removeItem(ADMIN_TOKEN_KEY)
    setAdminToken('')
  }

  return (
    <main>
      <h1>Viajes Aventura</h1>
      <p className="subtitulo">Sistema de gestión de agencia de viajes — TI3V21, INACAP Valparaíso</p>
      <Admin adminToken={adminToken} onSesionIniciada={iniciarSesionAdmin} onCerrarSesion={cerrarSesionAdmin} />
      <Clientes perfil={perfil} onSesionIniciada={iniciarSesion} onCerrarSesion={cerrarSesion} />
      <Destinos adminToken={adminToken} />
      <Paquetes adminToken={adminToken} />
      <Reservas token={token} perfil={perfil} />
    </main>
  )
}

export default App
