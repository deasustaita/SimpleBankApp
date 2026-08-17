import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { Customer, CustomerUpdatePayload } from '../types/customer';
import { deleteCurrentCustomer, getCurrentCustomer, loginCustomer, registerCustomer, updateCurrentCustomer } from '../api/customerApi';

interface AuthContextValue {
  customer: Customer | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, name: string, email: string) => Promise<void>;
  updateProfile: (updates: CustomerUpdatePayload) => Promise<Customer>;
  deleteMyAccount: () => Promise<void>;
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
    const token = localStorage.getItem('sb_access_token');

    if (!token) {
      localStorage.removeItem('sb_customer');
      setLoading(false);
      return;
    }

    if (saved) {
      try {
        setCustomer(JSON.parse(saved)); 
      } catch (error) {
        console.error('Failed to restore customer from localStorage', error);
        localStorage.removeItem('sb_customer'); 
      }
    }

    getCurrentCustomer()
      .then((profile) => {
        setCustomer(profile);
        localStorage.setItem('sb_customer', JSON.stringify(profile));
      })
      .catch(() => {
        localStorage.removeItem('sb_access_token');
        localStorage.removeItem('sb_customer');
        setCustomer(null);
      })
      .finally(() => {
        setLoading(false);
      });
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
      await registerCustomer({ username, password, name, email });

      const result = await loginCustomer({ username, password });
      setCustomer(result);
      localStorage.setItem('sb_customer', JSON.stringify(result));
    } catch (error) {
      throw error;
    }
  };


  const logout = () => {
    setCustomer(null); 
    localStorage.removeItem('sb_access_token');
    localStorage.removeItem('sb_customer');
  };

  const updateProfile = async (updates: CustomerUpdatePayload) => {
    const updated = await updateCurrentCustomer(updates);
    setCustomer(updated);
    localStorage.setItem('sb_customer', JSON.stringify(updated));
    return updated;
  };

  const deleteMyAccount = async () => {
    await deleteCurrentCustomer();
    setCustomer(null);
    localStorage.removeItem('sb_access_token');
    localStorage.removeItem('sb_customer');
  };


  return (
    <AuthContext.Provider value={{ customer, login, register, updateProfile, deleteMyAccount, logout, loading }}>
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