import { useState } from 'react'
import { IconChevronDown, IconShield } from './icons'

const formVacio = { correo: '', password: '' }

function Admin({ adminToken, onSesionIniciada, onCerrarSesion }) {
  const [abierto, setAbierto] = useState(false)
  const [form, setForm] = useState(formVacio)
  const [error, setError] = useState('')

  const iniciarSesion = async (e) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      setError(data.detail || 'No se pudo iniciar sesión')
      return
    }
    onSesionIniciada(data.access_token)
    setForm(formVacio)
    setAbierto(false)
  }

  return (
    <div className="auth-widget">
      <button className={`chip ${adminToken ? 'chip-on' : ''}`} onClick={() => setAbierto((v) => !v)}>
        <IconShield />
        <span>{adminToken ? 'Administrador' : 'Admin'}</span>
        <IconChevronDown className="chip-caret" />
      </button>

      {abierto && (
        <div className="auth-panel">
          {adminToken ? (
            <>
              <p className="auth-panel-title">Sesión de administrador activa</p>
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
            <form onSubmit={iniciarSesion} className="auth-form">
              <input
                type="email"
                placeholder="Correo de administrador"
                value={form.correo}
                onChange={(e) => setForm({ ...form, correo: e.target.value })}
                required
              />
              <input
                type="password"
                placeholder="Contraseña"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />
              <button type="submit">Iniciar sesión</button>
            </form>
          )}
          {error && <p className="error">{error}</p>}
        </div>
      )}
    </div>
  )
}

export default Admin
