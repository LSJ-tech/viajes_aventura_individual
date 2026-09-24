import { useEffect, useState } from 'react'

function Reservas({ token, perfil }) {
  const [paquetesPublicados, setPaquetesPublicados] = useState([])
  const [misReservas, setMisReservas] = useState([])
  const [paqueteId, setPaqueteId] = useState('')
  const [personas, setPersonas] = useState('1')
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(true)

  const cargarPaquetesPublicados = () => {
    fetch('/api/paquetes')
      .then((res) => res.json())
      .then((data) => setPaquetesPublicados(data.filter((p) => p.publicado)))
  }

  const cargarMisReservas = () => {
    if (!token) {
      setMisReservas([])
      setCargando(false)
      return
    }
    setCargando(true)
    fetch('/api/reservas', { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => res.json())
      .then(setMisReservas)
      .finally(() => setCargando(false))
  }

  useEffect(cargarPaquetesPublicados, [])
  useEffect(cargarMisReservas, [token])

  const reservar = async (e) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/reservas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ paquete_id: Number(paqueteId), personas: Number(personas) }),
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      setError(data.detail || 'No se pudo crear la reserva')
      return
    }
    setPaqueteId('')
    setPersonas('1')
    cargarPaquetesPublicados()
    cargarMisReservas()
  }

  if (!perfil) {
    return (
      <section>
        <h2>Reservas</h2>
        <p>Inicia sesión para reservar un paquete y ver tu historial.</p>
      </section>
    )
  }

  return (
    <section>
      <h2>Reservas</h2>

      <form onSubmit={reservar} className="form-destino">
        <select value={paqueteId} onChange={(e) => setPaqueteId(e.target.value)} required>
          <option value="">Elige un paquete publicado</option>
          {paquetesPublicados.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nombre} — ${p.precio} — {p.cupo_disponible} cupo(s)
            </option>
          ))}
        </select>
        <input
          type="number"
          min="1"
          placeholder="Cantidad de personas"
          value={personas}
          onChange={(e) => setPersonas(e.target.value)}
          required
        />
        <button type="submit">Reservar</button>
      </form>

      {error && <p className="error">{error}</p>}

      <h3>Mis reservas</h3>
      {cargando ? (
        <p>Cargando reservas...</p>
      ) : misReservas.length === 0 ? (
        <p>Todavía no tienes reservas.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Paquete</th>
              <th>Fechas</th>
              <th>Personas</th>
              <th>Total</th>
              <th>Emitida</th>
            </tr>
          </thead>
          <tbody>
            {misReservas.map((r) => (
              <tr key={r.id}>
                <td>{r.paquete.nombre}</td>
                <td>
                  {r.paquete.fecha_salida} → {r.paquete.fecha_regreso}
                </td>
                <td>{r.personas}</td>
                <td>${r.total}</td>
                <td>{r.fecha_emision}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default Reservas
