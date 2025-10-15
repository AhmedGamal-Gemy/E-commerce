'use client';
import { create } from 'zustand';
import Cookies from 'js-cookie';

export const useAuthStore = create((set) => ({
  token: Cookies.get('auth_token') || null,
  user: Cookies.get('auth_user') ? JSON.parse(Cookies.get('auth_user')) : null,
  message: null,
  loading: false,

  setMessage: (message) => set({ message }),
  setLoading: (loading) => set({ loading }),

  login: (token, user) => {
    Cookies.set('auth_token', token, { expires: 7, secure: true });
    Cookies.set('auth_user', JSON.stringify(user), { expires: 7, secure: true });
    set({ token, user });
  },

  logout: () => {
    Cookies.remove('auth_token');
    Cookies.remove('auth_user');
    set({ token: null, user: null });
  },

  updateUser: (updatedUser) => {
    Cookies.set('auth_user', JSON.stringify(updatedUser), { expires: 7, secure: true });
    set({ user: updatedUser });
  },

}));
