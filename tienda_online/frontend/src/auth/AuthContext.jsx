import { createContext, useContext, useEffect, useState } from 'react'
import { getMe, login as loginRequest } from '../api/client'

const AuthContext = createContext(null)
const TOKEN_KEY = 'tunto.access'

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(token))

  useEffect(() => {
    if (!token) { setLoading(false); return }
    getMe(token).then(setUser).catch(() => {
      localStorage.removeItem(TOKEN_KEY)
      setToken(null)
      setUser(null)
    }).finally(() => setLoading(false))
  }, [token])

  async function signIn(credentials) {
    const tokens = await loginRequest(credentials)
    localStorage.setItem(TOKEN_KEY, tokens.access)
    setToken(tokens.access)
    const profile = await getMe(tokens.access)
    setUser(profile)
    return tokens.access
  }

  function signOut() {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    setUser(null)
  }

  return <AuthContext.Provider value={{ token, user, loading, signIn, signOut }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return context
}
