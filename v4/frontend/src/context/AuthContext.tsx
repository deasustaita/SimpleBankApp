import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { Customer } from '../types/customer';
import { loginCustomer, registerCustomer } from '../api/customerApi';

interface AuthContextValue {
  customer: Customer | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, name: string, email: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);


interface AuthProviderProps {
  children: ReactNode;
}


export function AuthProvider({ children }: AuthProviderProps) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem('sb_customer');
    if (saved) {
      try {
        setCustomer(JSON.parse(saved)); 
      } catch (error) {
        console.error('Failed to restore customer from localStorage', error);
        localStorage.removeItem('sb_customer'); 
      }
    }
    setLoading(false); 
  }, []); 


  const login = async (username: string, password: string) => {
    try {
      const result = await loginCustomer({ username, password }); 
      setCustomer(result);
      localStorage.setItem('sb_customer', JSON.stringify(result)); 
    } catch (error) {
      throw error; 
    }
  };


  const register = async (username: string, password: string, name: string, email: string) => {
    try {
      const result = await registerCustomer({ username, password, name, email });
      setCustomer(result); 
      localStorage.setItem('sb_customer', JSON.stringify(result)); 
    } catch (error) {
      throw error;
    }
  };


  const logout = () => {
    setCustomer(null); 
    localStorage.removeItem('sb_customer');
  };


  return (
    <AuthContext.Provider value={{ customer, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used inside <AuthProvider>');
  }
  return context;
}