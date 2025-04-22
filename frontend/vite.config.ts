import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, './config', '');

  const viteEnvVars = Object.fromEntries(
    Object.entries(env).filter(([key]) => key.startsWith('VITE_'))
  );

  const metaEnv = {
    ...Object.fromEntries(
      Object.entries(viteEnvVars).map(([key, val]) => ['import.meta.env.' + key, JSON.stringify(val)])
    )
  };

  return {
    plugins: [react()],
    define: metaEnv
  };
});