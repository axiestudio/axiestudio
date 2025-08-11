/**
 * API utilities for internationalization
 * Automatically adds language headers to API requests
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import i18n from '../i18n';

// Create an axios instance with automatic language header injection
export const createI18nAxiosInstance = (baseURL?: string): AxiosInstance => {
  const instance = axios.create({
    baseURL: baseURL || process.env.REACT_APP_API_URL || '/api',
    timeout: 30000,
  });

  // Request interceptor to add language header
  instance.interceptors.request.use(
    (config) => {
      // Add current language to headers
      const currentLanguage = i18n.language || 'en';
      config.headers['Accept-Language'] = currentLanguage;
      config.headers['X-Language'] = currentLanguage;
      
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor to handle translated error messages
  instance.interceptors.response.use(
    (response: AxiosResponse) => {
      return response;
    },
    (error) => {
      // Error responses should already be translated by the backend
      // but we can add additional handling here if needed
      if (error.response?.data?.detail) {
        // The backend should return translated error messages
        // based on the Accept-Language header
        console.debug('Received translated error:', error.response.data.detail);
      }
      
      return Promise.reject(error);
    }
  );

  return instance;
};

// Default i18n-enabled axios instance
export const apiClient = createI18nAxiosInstance();

// Hook for making API calls with automatic language headers
export const useI18nApi = () => {
  const makeRequest = async <T = any>(
    config: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    return apiClient.request<T>(config);
  };

  const get = async <T = any>(
    url: string, 
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    return apiClient.get<T>(url, config);
  };

  const post = async <T = any>(
    url: string, 
    data?: any, 
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    return apiClient.post<T>(url, data, config);
  };

  const put = async <T = any>(
    url: string, 
    data?: any, 
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    return apiClient.put<T>(url, data, config);
  };

  const patch = async <T = any>(
    url: string, 
    data?: any, 
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    return apiClient.patch<T>(url, data, config);
  };

  const del = async <T = any>(
    url: string, 
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    return apiClient.delete<T>(url, config);
  };

  return {
    request: makeRequest,
    get,
    post,
    put,
    patch,
    delete: del,
  };
};

// Utility function to get current language
export const getCurrentLanguage = (): string => {
  return i18n.language || 'en';
};

// Utility function to check if a language is supported
export const isSupportedLanguage = (lang: string): boolean => {
  const supportedLanguages = ['en', 'sv']; // Add more as needed
  return supportedLanguages.includes(lang);
};

// Function to update API client language (useful when language changes)
export const updateApiLanguage = (language: string): void => {
  // This will be automatically handled by the request interceptor
  // but we can add any additional logic here if needed
  console.debug(`API language updated to: ${language}`);
};

// Error message extractor that handles both English and translated responses
export const extractErrorMessage = (error: any): string => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  
  if (error.message) {
    return error.message;
  }
  
  // Fallback to generic error message
  return 'An unexpected error occurred';
};

// Type definitions for API responses
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

// Helper function to create API error responses
export const createApiError = (
  message: string, 
  code?: string, 
  field?: string
): ApiError => {
  return {
    detail: message,
    code,
    field,
  };
};

// Helper function to create API success responses
export const createApiResponse = <T>(
  data: T, 
  message?: string
): ApiResponse<T> => {
  return {
    success: true,
    data,
    message,
  };
};
