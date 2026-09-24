import { useState } from 'react'

const formVacio = { correo: '', password: '' }

function Admin({ adminToken, onSesionIniciada, onCerrarSesion }) {
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
  }

  if (adminToken) {
    return (
      <section>
        <h2>Administración</h2>
        <p>Sesión de administrador activa. Ahora puedes crear destinos y paquetes más abajo.</p>
        <button onClick={onCerrarSesion}>Cerrar sesión de administrador</button>
      </section>
    )
  }

  return (
    <section>
      <h2>Administración</h2>
      <form onSubmit={iniciarSesion} className="form-destino">
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
      {error && <p className="error">{error}</p>}
    </section>
  )
}

export default Admin
