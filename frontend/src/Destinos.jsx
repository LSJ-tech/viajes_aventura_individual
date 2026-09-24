import { useEffect, useState } from 'react'

const formVacio = { nombre: '', zona: '', descripcion: '', duracion_dias: '', costo_base: '' }

function Destinos({ adminToken }) {
  const [destinos, setDestinos] = useState([])
  const [form, setForm] = useState(formVacio)
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(true)

  const cargarDestinos = () => {
    fetch('/api/destinos')
      .then((res) => res.json())
      .then(setDestinos)
      .catch(() => setError('No se pudo cargar el catálogo de destinos'))
      .finally(() => setCargando(false))
  }

  useEffect(cargarDestinos, [])

  const actualizarCampo = (campo) => (e) => {
    setForm({ ...form, [campo]: e.target.value })
  }

  const crearDestino = async (e) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/destinos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${adminToken}` },
      body: JSON.stringify({
        ...form,
        duracion_dias: Number(form.duracion_dias),
        costo_base: Number(form.costo_base),
      }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setError(data.detail || 'No se pudo crear el destino')
      return
    }
    setForm(formVacio)
    cargarDestinos()
  }

  const eliminarDestino = async (id) => {
    // El id siempre viene de un destino ya listado por el backend, pero se valida
    // igual antes de usarlo en la URL (nunca confiar en el dato tal cual llega).
    const destinoId = Number(id)
    if (!Number.isInteger(destinoId) || destinoId < 0) return

    const res = await fetch(`/api/destinos/${destinoId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${adminToken}` },
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setError(data.detail || 'No se pudo eliminar el destino')
      return
    }
    cargarDestinos()
  }

  let tablaDestinos
  if (cargando) {
    tablaDestinos = <p className="estado-vacio">Cargando destinos…</p>
  } else if (destinos.length === 0) {
    tablaDestinos = <p className="estado-vacio">Todavía no hay destinos en el catálogo.</p>
  } else {
    tablaDestinos = (
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Zona</th>
              <th>Duración</th>
              <th>Costo base</th>
              <th>Estado</th>
              {adminToken && <th></th>}
            </tr>
          </thead>
          <tbody>
            {destinos.map((d) => (
              <tr key={d.id}>
                <td data-label="Nombre">{d.nombre}</td>
                <td data-label="Zona">{d.zona}</td>
                <td data-label="Duración">{d.duracion_dias} días</td>
                <td data-label="Costo base">${d.costo_base}</td>
                <td data-label="Estado">
                  <span className={`badge ${d.disponible ? 'badge-ok' : 'badge-off'}`}>
                    {d.disponible ? 'Disponible' : 'No disponible'}
                  </span>
                </td>
                {adminToken && (
                  <td>
                    <button onClick={() => eliminarDestino(d.id)}>Eliminar</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <section>
      <h2>Catálogo de destinos</h2>

      {adminToken && (
        <form onSubmit={crearDestino} className="form-destino">
          <input placeholder="Nombre" value={form.nombre} onChange={actualizarCampo('nombre')} required />
          <input placeholder="Zona" value={form.zona} onChange={actualizarCampo('zona')} required />
          <input
            placeholder="Descripción"
            value={form.descripcion}
            onChange={actualizarCampo('descripcion')}
            required
          />
          <input
            type="number"
            min="1"
            placeholder="Duración (días)"
            value={form.duracion_dias}
            onChange={actualizarCampo('duracion_dias')}
            required
          />
          <input
            type="number"
            min="1"
            placeholder="Costo base"
            value={form.costo_base}
            onChange={actualizarCampo('costo_base')}
            required
          />
          <button type="submit">Agregar destino</button>
        </form>
      )}

      {error && <p className="error">{error}</p>}

      {tablaDestinos}
    </section>
  )
}

export default Destinos
