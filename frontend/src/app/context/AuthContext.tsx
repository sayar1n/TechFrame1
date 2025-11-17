'use client';

import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { loginUser, registerUser, getMe } from '../api/auth'; // Предполагается, что эти функции будут созданы
import { User, LoginData, RegisterData } from '../types'; // Предполагается, что эти типы будут созданы

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    const loadUserFromStorage = () => {
      try {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          // Загружаем актуальные данные пользователя при инициализации
          getMe(storedToken).then(userResponse => {
            setUser(userResponse);
          }).catch(error => {
            console.error("Failed to fetch user on init:", error);
            logout(); // Выходим, если токен недействителен или ошибка
          });
        }
      } catch (error) {
        console.error('Failed to load user from storage:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadUserFromStorage();
  }, []);

  const login = async (data: LoginData) => {
    setIsLoading(true);
    try {
      const response = await loginUser(data);
      setToken(response.access_token);
      localStorage.setItem('token', response.access_token);

      // Получаем актуальные данные пользователя после входа
      const fetchedUser = await getMe(response.access_token);
      setUser(fetchedUser);
      localStorage.setItem('user', JSON.stringify(fetchedUser));
      router.push('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setIsLoading(true);
    try {
      const newUser = await registerUser(data);
      // После регистрации можно сразу залогинить пользователя или перенаправить на страницу логина
      // await login({ username: data.username, password: data.password });
      router.push('/login');
      return newUser;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
