// Axie Studio Backend Configuration
// Check if we're in Tauri environment
const isTauri = typeof window !== 'undefined' && '__TAURI__' in window;

// Production backend URL - Updated to match your architecture
const PRODUCTION_BACKEND_URL = 'https://flow.axiestudio.se';

// Development backend URL
const DEVELOPMENT_BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:7860';

// Determine the correct base URL based on environment
export const baseURL = (() => {
  // In production builds (including Tauri), use production backend
  if (process.env.NODE_ENV === 'production' || isTauri) {
    return PRODUCTION_BACKEND_URL;
  }

  // In development, use environment variable or localhost
  return DEVELOPMENT_BACKEND_URL;
})();

console.log('🔗 Backend URL configured:', {
  baseURL,
  isTauri,
  nodeEnv: process.env.NODE_ENV,
  backendEnv: process.env.BACKEND_URL
});
