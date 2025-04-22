
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export interface AuthState {
  bearerToken: string | null;
  setBearerToken: (refreshToken: string) => void;
  hasBearerToken: () => boolean;
  logout: () => void;
}

export const useAuthStateStore = create<AuthState>()(
  persist(
    (set, get) => ({
      bearerToken: null,
      setBearerToken: (bearerToken: string) => set(() => ({ bearerToken })),
      hasBearerToken: () => get().bearerToken !== null,
      logout() {
        set(() => ({ bearerToken: null }));
      }
    }),
    {
      name: 'auth',
      storage: createJSONStorage(() => localStorage)
    }
  )
);
