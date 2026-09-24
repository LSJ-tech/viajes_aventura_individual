import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [estado, setEstado] = useState('Conectando con el backend...')

  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => setEstado(`Backend OK: ${data.status}`))
      .catch(() => setEstado('No se pudo conectar con el backend'))
  }, [])

  return (
    <main>
      <h1>Viajes Aventura</h1>
      <p>{estado}</p>
    </main>
  )
}

export default App
