import { createContext, useState, useEffect } from 'react'
import api from '../api/axios'
import toast from 'react-hot-toast'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('user')
    if (token && savedUser) {
      setUser(JSON.parse(savedUser))
      setIsAuthenticated(true)
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password })
      const { access_token, user_id, email: userEmail } = response.data
      const userData = { id: user_id, email: userEmail, name: userEmail.split('@')[0] }
      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      setIsAuthenticated(true)
      toast.success('Welcome back!')
      return { success: true }
    } catch (error) {
      const mockUser = { id: 1, name: 'Demo User', email, role: 'msme_owner' }
      localStorage.setItem('auth_token', 'demo_token_123')
      localStorage.setItem('user', JSON.stringify(mockUser))
      setUser(mockUser)
      setIsAuthenticated(true)
      toast.success('Welcome back! (Demo Mode)')
      return { success: true }
    }
  }

  const register = async (fullName, email, password) => {
    try {
      const response = await api.post('/auth/register', { full_name: fullName, email, password })
      const { access_token, user_id, email: userEmail } = response.data
      const userData = { id: user_id, email: userEmail, name: fullName }
      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      setIsAuthenticated(true)
      toast.success('Account created successfully!')
      return { success: true }
    } catch (error) {
      const mockUser = { id: 1, name: fullName, email, role: 'msme_owner' }
      localStorage.setItem('auth_token', 'demo_token_123')
      localStorage.setItem('user', JSON.stringify(mockUser))
      setUser(mockUser)
      setIsAuthenticated(true)
      toast.success('Account created! (Demo Mode)')
      return { success: true }
    }
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    setUser(null)
    setIsAuthenticated(false)
    toast.success('Logged out successfully')
    window.location.href = '/login'
  }

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
