import { useState } from 'react'

const registroVacio = { nombre: '', rut: '', correo: '', telefono: '', password: '' }
const loginVacio = { correo: '', password: '' }

function Clientes({ perfil, onSesionIniciada, onCerrarSesion }) {
  const [modo, setModo] = useState('login')
  const [formRegistro, setFormRegistro] = useState(registroVacio)
  const [formLogin, setFormLogin] = useState(loginVacio)
  const [error, setError] = useState('')

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
    onSesionIniciada(data)
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
    onSesionIniciada(data)
    setFormLogin(loginVacio)
  }

  if (perfil) {
    return (
      <section>
        <h2>Mi cuenta</h2>
        <p>
          Sesión iniciada como <strong>{perfil.nombre}</strong> ({perfil.correo}).
        </p>
        <button onClick={onCerrarSesion}>Cerrar sesión</button>
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
