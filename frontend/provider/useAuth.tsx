"use client"

import { AuthContextType, User } from "@/types"
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useReducer,
} from "react"

// Define action types
type AuthAction =
  | { type: "SET_INITIAL_STATE"; payload: User }
  | { type: "INITIALIZATION_COMPLETE" }
  | { type: "LOGIN_START" }
  | { type: "LOGIN_SUCCESS"; payload: { token: string; user: User } }
  | { type: "LOGIN_ERROR"; payload: string }
  | { type: "LOGOUT" }

// Define state type
interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoggedIn: boolean
  userRole: string | null
  isLoading: boolean
  loginError: string | null
  isInitializing: boolean
}

// Initial state
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoggedIn: false,
  userRole: null,
  isLoading: false,
  loginError: null,
  isInitializing: true,
}

// Reducer function
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case "SET_INITIAL_STATE":
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoggedIn: true,
        userRole: action.payload.role,
        isInitializing: false,
      }

    case "INITIALIZATION_COMPLETE":
      return {
        ...state,
        isInitializing: false,
      }

    case "LOGIN_START":
      return {
        ...state,
        isLoading: true,
        loginError: null,
      }

    case "LOGIN_SUCCESS":
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoggedIn: true,
        userRole: action.payload.user.role,
        isLoading: false,
        loginError: null,
      }

    case "LOGIN_ERROR":
      return {
        ...state,
        isLoading: false,
        loginError: action.payload,
        user: null,
        isAuthenticated: false,
        isLoggedIn: false,
        userRole: null,
      }

    case "LOGOUT":
      return {
        ...initialState,
        isInitializing: false,
      }

    default:
      return state
  }
}

// Create context
export const AuthContext = createContext<AuthContextType>({} as AuthContextType)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, dispatch] = useReducer(authReducer, initialState)

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedUser = localStorage.getItem("user")
        const token = localStorage.getItem("token")

        if (storedUser && token) {
          const parsedUser: User = JSON.parse(storedUser)
          dispatch({ type: "SET_INITIAL_STATE", payload: parsedUser })
        } else {
          dispatch({ type: "INITIALIZATION_COMPLETE" })
        }
      } catch (error) {
        console.error("Error during initialization:", error)
        localStorage.removeItem("user")
        localStorage.removeItem("token")
        dispatch({ type: "INITIALIZATION_COMPLETE" })
      }
    }

    initializeAuth()
  }, [])

  const handleLogout = useCallback(() => {
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    dispatch({ type: "LOGOUT" })
  }, [])

  const handleLogin = useCallback(
    async (token: string, userData: User) => {
      dispatch({ type: "LOGIN_START" })
      try {
        // await new Promise((resolve) => setTimeout(resolve, 1000));
        localStorage.setItem("token", token)
        localStorage.setItem("user", JSON.stringify(userData))
        dispatch({
          type: "LOGIN_SUCCESS",
          payload: { token, user: userData },
        })
      } catch (error) {
        dispatch({
          type: "LOGIN_ERROR",
          payload: error instanceof Error ? error.message : "Login failed",
        })
        handleLogout()
      }
    },
    [handleLogout],
  )

  const hasRole = useCallback(
    (role: string): boolean => {
      return state.userRole === role
    },
    [state.userRole],
  )

  const contextValue: AuthContextType = {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoggedIn: state.isLoggedIn,
    userRole: state.userRole,
    login: handleLogin,
    logout: handleLogout,
    hasRole,
    isLoading: state.isLoading,
    loginError: state.loginError,
    isInitializing: state.isInitializing,
  }

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  )
}

export const useAuth = () => {
  const auth = useContext(AuthContext)
  if (!auth) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return auth
}
