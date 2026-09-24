import { useEffect, useState } from 'react'
import './App.css'
import Clientes from './Clientes'
import Destinos from './Destinos'
import Paquetes from './Paquetes'
import Reservas from './Reservas'

const TOKEN_KEY = 'viajes_aventura_token'

function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [perfil, setPerfil] = useState(null)

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

  return (
    <main>
      <h1>Viajes Aventura</h1>
      <Clientes perfil={perfil} onSesionIniciada={iniciarSesion} onCerrarSesion={cerrarSesion} />
      <Destinos />
      <Paquetes />
      <Reservas token={token} perfil={perfil} />
    </main>
  )
}

export default App
