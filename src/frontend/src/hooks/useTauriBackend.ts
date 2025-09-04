import { useEffect, useState } from 'react';

// Tauri API types
interface TauriAPI {
  invoke: (command: string, args?: any) => Promise<any>;
}

interface ApiConfig {
  backend_url: string;
  timeout: number;
}

interface HealthResponse {
  status: string;
}

// Check if we're running in Tauri
const isTauri = () => {
  return typeof window !== 'undefined' && '__TAURI__' in window;
};

// Get Tauri API
const getTauriAPI = (): TauriAPI | null => {
  if (isTauri()) {
    return (window as any).__TAURI__.core;
  }
  return null;
};

export const useTauriBackend = () => {
  const [isInTauri, setIsInTauri] = useState(false);
  const [backendUrl, setBackendUrl] = useState<string>('');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(false);
  const [apiConfig, setApiConfig] = useState<ApiConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTauriBackend = async () => {
      try {
        setLoading(true);
        setError(null);

        // Check if we're in Tauri
        const tauriDetected = isTauri();
        setIsInTauri(tauriDetected);

        if (tauriDetected) {
          const tauri = getTauriAPI();
          if (tauri) {
            // Get backend URL from Tauri
            const url = await tauri.invoke('get_backend_url');
            setBackendUrl(url);

            // Get API configuration
            const config = await tauri.invoke('get_api_config');
            setApiConfig(config);

            // Check backend health
            try {
              const health = await tauri.invoke('check_backend_health');
              setIsBackendHealthy(health.status === 'ok');
            } catch (healthError) {
              console.warn('Backend health check failed:', healthError);
              setIsBackendHealthy(false);
            }

            console.log('🚀 Tauri Backend Integration Initialized:', {
              backendUrl: url,
              config,
              isHealthy: isBackendHealthy
            });
          }
        } else {
          // Fallback for web version
          const webBackendUrl = process.env.BACKEND_URL || 'https://flow.axiestudio.se';
          setBackendUrl(webBackendUrl);
          setApiConfig({
            backend_url: webBackendUrl,
            timeout: 30000
          });

          // Simple health check for web version
          try {
            const response = await fetch(`${webBackendUrl}/health`);
            const health = await response.json();
            setIsBackendHealthy(health.status === 'ok');
          } catch (healthError) {
            console.warn('Web backend health check failed:', healthError);
            setIsBackendHealthy(false);
          }

          console.log('🌐 Web Backend Integration Initialized:', {
            backendUrl: webBackendUrl,
            isHealthy: isBackendHealthy
          });
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Unknown error';
        setError(errorMessage);
        console.error('❌ Backend integration failed:', err);
      } finally {
        setLoading(false);
      }
    };

    initializeTauriBackend();
  }, []);

  const checkHealth = async (): Promise<boolean> => {
    try {
      if (isInTauri) {
        const tauri = getTauriAPI();
        if (tauri) {
          const health = await tauri.invoke('check_backend_health');
          const healthy = health.status === 'ok';
          setIsBackendHealthy(healthy);
          return healthy;
        }
      } else {
        const response = await fetch(`${backendUrl}/health`);
        const health = await response.json();
        const healthy = health.status === 'ok';
        setIsBackendHealthy(healthy);
        return healthy;
      }
    } catch (error) {
      console.error('Health check failed:', error);
      setIsBackendHealthy(false);
      return false;
    }
    return false;
  };

  const getEffectiveBackendUrl = (): string => {
    if (isInTauri && backendUrl) {
      return backendUrl;
    }
    return process.env.BACKEND_URL || 'https://flow.axiestudio.se';
  };

  return {
    isInTauri,
    backendUrl: getEffectiveBackendUrl(),
    isBackendHealthy,
    apiConfig,
    loading,
    error,
    checkHealth,
    // Utility functions
    isTauriEnvironment: isInTauri,
    isWebEnvironment: !isInTauri,
  };
};

// Export utility functions
export const isTauriApp = () => isTauri();
export const getTauriCore = () => getTauriAPI();

export default useTauriBackend;
