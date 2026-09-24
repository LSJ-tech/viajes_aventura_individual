import { useState } from 'react'
import { IconChevronDown, IconUser } from './icons'

const registroVacio = { nombre: '', rut: '', correo: '', telefono: '', password: '' }
const loginVacio = { correo: '', password: '' }

function Clientes({ perfil, onSesionIniciada, onCerrarSesion }) {
  const [abierto, setAbierto] = useState(false)
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
    setAbierto(false)
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
    setAbierto(false)
  }

  return (
    <div className="auth-widget">
      <button className={`chip ${perfil ? 'chip-on' : ''}`} onClick={() => setAbierto((v) => !v)}>
        <IconUser />
        <span>{perfil ? perfil.nombre.split(' ')[0] : 'Mi cuenta'}</span>
        <IconChevronDown className="chip-caret" />
      </button>

      {abierto && (
        <div className="auth-panel">
          {perfil ? (
            <>
              <p className="auth-panel-title">
                {perfil.nombre} · {perfil.correo}
              </p>
              <button
                className="btn-ghost"
                onClick={() => {
                  onCerrarSesion()
                  setAbierto(false)
                }}
              >
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <div className="tabs tabs-compact">
                <button type="button" onClick={() => setModo('login')} disabled={modo === 'login'}>
                  Iniciar sesión
                </button>
                <button type="button" onClick={() => setModo('registro')} disabled={modo === 'registro'}>
                  Registrarme
                </button>
              </div>

              {modo === 'login' ? (
                <form onSubmit={iniciarSesion} className="auth-form">
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
                <form onSubmit={registrar} className="auth-form">
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
            </>
          )}
          {error && <p className="error">{error}</p>}
        </div>
      )}
    </div>
  )
}

export default Clientes
