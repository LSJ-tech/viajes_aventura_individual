import { useEffect, useState } from 'react'

const formVacio = { nombre: '', fecha_salida: '', fecha_regreso: '', cupo_maximo: '', margen: '0.20' }

function Paquetes({ adminToken }) {
  const [paquetes, setPaquetes] = useState([])
  const [destinosDisponibles, setDestinosDisponibles] = useState([])
  const [seleccionados, setSeleccionados] = useState([])
  const [form, setForm] = useState(formVacio)
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(true)

  const cargarPaquetes = () => {
    fetch('/api/paquetes')
      .then((res) => res.json())
      .then(setPaquetes)
      .catch(() => setError('No se pudo cargar el catálogo de paquetes'))
      .finally(() => setCargando(false))
  }

  const cargarDestinosDisponibles = () => {
    fetch('/api/destinos?solo_disponibles=true')
      .then((res) => res.json())
      .then(setDestinosDisponibles)
  }

  useEffect(() => {
    cargarPaquetes()
    cargarDestinosDisponibles()
  }, [])

  const actualizarCampo = (campo) => (e) => setForm({ ...form, [campo]: e.target.value })

  const alternarDestino = (id) => {
    setSeleccionados((prev) => (prev.includes(id) ? prev.filter((d) => d !== id) : [...prev, id]))
  }

  const crearPaquete = async (e) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/paquetes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${adminToken}` },
      body: JSON.stringify({
        ...form,
        cupo_maximo: Number(form.cupo_maximo),
        margen: Number(form.margen),
        destino_ids: seleccionados,
      }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setError(typeof data.detail === 'string' ? data.detail : 'No se pudo crear el paquete (revisa los destinos elegidos)')
      return
    }
    setForm(formVacio)
    setSeleccionados([])
    cargarPaquetes()
    cargarDestinosDisponibles()
  }

  const publicarPaquete = async (id) => {
    setError('')
    const res = await fetch(`/api/paquetes/${id}/publicar`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${adminToken}` },
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setError(data.detail || 'No se pudo publicar el paquete')
      return
    }
    cargarPaquetes()
  }

  return (
    <section>
      <h2>Paquetes</h2>

      {adminToken && (
        <form onSubmit={crearPaquete} className="form-destino">
          <input placeholder="Nombre" value={form.nombre} onChange={actualizarCampo('nombre')} required />
          <input type="date" value={form.fecha_salida} onChange={actualizarCampo('fecha_salida')} required />
          <input type="date" value={form.fecha_regreso} onChange={actualizarCampo('fecha_regreso')} required />
          <input
            type="number"
            min="1"
            placeholder="Cupo máximo"
            value={form.cupo_maximo}
            onChange={actualizarCampo('cupo_maximo')}
            required
          />
          <input
            type="number"
            step="0.01"
            min="0"
            placeholder="Margen (0.20 = 20%)"
            value={form.margen}
            onChange={actualizarCampo('margen')}
            required
          />

          <fieldset className="fieldset-destinos">
            <legend>Destinos (elige entre 2 y 5)</legend>
            {destinosDisponibles.map((d) => (
              <label key={d.id}>
                <input
                  type="checkbox"
                  checked={seleccionados.includes(d.id)}
                  onChange={() => alternarDestino(d.id)}
                />
                {d.nombre} (${d.costo_base})
              </label>
            ))}
          </fieldset>

          <button type="submit">Crear paquete</button>
        </form>
      )}

      {error && <p className="error">{error}</p>}

      {cargando ? (
        <p className="estado-vacio">Cargando paquetes…</p>
      ) : paquetes.length === 0 ? (
        <p className="estado-vacio">Todavía no hay paquetes creados.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Fechas</th>
                <th>Destinos</th>
                <th>Cupo disp.</th>
                <th>Precio</th>
                <th>Estado</th>
                {adminToken && <th></th>}
              </tr>
            </thead>
            <tbody>
              {paquetes.map((p) => (
                <tr key={p.id}>
                  <td data-label="Nombre">{p.nombre}</td>
                  <td data-label="Fechas">
                    {p.fecha_salida} → {p.fecha_regreso}
                  </td>
                  <td data-label="Destinos">{p.destinos.map((d) => d.nombre).join(', ')}</td>
                  <td data-label="Cupo disp.">{p.cupo_disponible}</td>
                  <td data-label="Precio">${p.precio}</td>
                  <td data-label="Estado">
                    <span className={`badge ${p.publicado ? 'badge-ok' : 'badge-warn'}`}>
                      {p.publicado ? 'Publicado' : 'Borrador'}
                    </span>
                  </td>
                  {adminToken && (
                    <td>
                      {!p.publicado && (
                        <button className="btn-publicar" onClick={() => publicarPaquete(p.id)}>
                          Publicar
                        </button>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default Paquetes
