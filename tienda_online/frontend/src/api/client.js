const API = '/api'

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = data.detail || Object.values(data).flat().join(' ')
    throw new Error(detail || `La solicitud falló (${response.status})`)
  }
  return data
}

export const login = (payload) => request('/auth/token/', { method: 'POST', body: JSON.stringify(payload) })
export const register = (payload) => request('/auth/register/', { method: 'POST', body: JSON.stringify(payload) })
export const getMe = (token) => request('/auth/me/', { headers: { Authorization: `Bearer ${token}` } })
export const getCountries = () => request('/soap/countries/')
export async function getCampusMoment() {
  const response = await fetch('https://dog.ceo/api/breeds/image/random')
  if (!response.ok) throw new Error('No se pudo consultar la API de imágenes.')
  return response.json()
}
