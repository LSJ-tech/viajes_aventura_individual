import { useEffect, useState } from 'react'

const TOKEN_KEY = 'viajes_aventura_token'

const registroVacio = { nombre: '', rut: '', correo: '', telefono: '', password: '' }
const loginVacio = { correo: '', password: '' }

function Clientes() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [perfil, setPerfil] = useState(null)
  const [modo, setModo] = useState('login')
  const [formRegistro, setFormRegistro] = useState(registroVacio)
  const [formLogin, setFormLogin] = useState(loginVacio)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!token) return
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const guardarSesion = (data) => {
    localStorage.setItem(TOKEN_KEY, data.access_token)
    setToken(data.access_token)
    setPerfil(data.cliente)
  }

  const registrar = async (e) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/clientes/registro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formRegistro),
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      setError(typeof data.detail === 'string' ? data.detail : 'No se pudo registrar la cuenta')
      return
    }
    guardarSesion(data)
    setFormRegistro(registroVacio)
  }

  const iniciarSesion = async (e) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/clientes/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formLogin),
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      setError(data.detail || 'No se pudo iniciar sesión')
      return
    }
    guardarSesion(data)
    setFormLogin(loginVacio)
  }

  const cerrarSesion = () => {
    localStorage.removeItem(TOKEN_KEY)
    setToken('')
    setPerfil(null)
  }

  if (perfil) {
    return (
      <section>
        <h2>Mi cuenta</h2>
        <p>
          Sesión iniciada como <strong>{perfil.nombre}</strong> ({perfil.correo}).
        </p>
        <button onClick={cerrarSesion}>Cerrar sesión</button>
      </section>
    )
  }

  return (
    <section>
      <h2>Mi cuenta</h2>
      <div className="tabs">
        <button type="button" onClick={() => setModo('login')} disabled={modo === 'login'}>
          Iniciar sesión
        </button>
        <button type="button" onClick={() => setModo('registro')} disabled={modo === 'registro'}>
          Registrarme
        </button>
      </div>

      {modo === 'login' ? (
        <form onSubmit={iniciarSesion} className="form-destino">
          <input
            type="email"
            placeholder="Correo"
            value={formLogin.correo}
            onChange={(e) => setFormLogin({ ...formLogin, correo: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={formLogin.password}
            onChange={(e) => setFormLogin({ ...formLogin, password: e.target.value })}
            required
          />
          <button type="submit">Iniciar sesión</button>
        </form>
      ) : (
        <form onSubmit={registrar} className="form-destino">
          <input
            placeholder="Nombre"
            value={formRegistro.nombre}
            onChange={(e) => setFormRegistro({ ...formRegistro, nombre: e.target.value })}
            required
          />
          <input
            placeholder="RUT (12345678-9)"
            value={formRegistro.rut}
            onChange={(e) => setFormRegistro({ ...formRegistro, rut: e.target.value })}
            required
          />
          <input
            type="email"
            placeholder="Correo"
            value={formRegistro.correo}
            onChange={(e) => setFormRegistro({ ...formRegistro, correo: e.target.value })}
            required
          />
          <input
            placeholder="Teléfono"
            value={formRegistro.telefono}
            onChange={(e) => setFormRegistro({ ...formRegistro, telefono: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Contraseña (mín. 8 caracteres)"
            value={formRegistro.password}
            onChange={(e) => setFormRegistro({ ...formRegistro, password: e.target.value })}
            required
          />
          <button type="submit">Crear cuenta</button>
        </form>
      )}

      {error && <p className="error">{error}</p>}
    </section>
  )
}

export default Clientes
