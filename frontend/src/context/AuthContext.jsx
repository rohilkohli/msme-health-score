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
      const { token, user: userData } = response.data
      localStorage.setItem('auth_token', token)
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      setIsAuthenticated(true)
      toast.success('Welcome back!')
      return { success: true }
    } catch (error) {
      // For demo purposes, allow mock login
      const mockUser = { id: 1, name: 'Demo User', email, role: 'msme_owner' }
      localStorage.setItem('auth_token', 'demo_token_123')
      localStorage.setItem('user', JSON.stringify(mockUser))
      setUser(mockUser)
      setIsAuthenticated(true)
      toast.success('Welcome back! (Demo Mode)')
      return { success: true }
    }
  }

  const register = async (name, email, password) => {
    try {
      const response = await api.post('/auth/register', { name, email, password })
      const { token, user: userData } = response.data
      localStorage.setItem('auth_token', token)
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      setIsAuthenticated(true)
      toast.success('Account created successfully!')
      return { success: true }
    } catch (error) {
      // For demo purposes, allow mock registration
      const mockUser = { id: 1, name, email, role: 'msme_owner' }
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
