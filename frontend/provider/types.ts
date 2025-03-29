export interface User {
  user_id: number
  username: string
  email: string
  full_name: string
  address: string
  phone: string
  role: string
  is_verified: boolean
}

export interface AuthResponse {
  access_token: string
  user: User
}

export interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoggedIn: boolean
  userRole: string | null
  isLoading: boolean
  loginError: string | null
  isInitializing: boolean
  logout: () => void
  hasRole: (role: string) => boolean
  login: (token: string, user: User) => void
}
