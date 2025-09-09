/**
 * Real-time Subscription Provider
 * Ensures subscription status is always up-to-date across the entire application
 */

import React, { createContext, useContext, useEffect, ReactNode } from 'react';
import { useRealtimeSubscription } from '@/hooks/useRealtimeSubscription';
import useAuthStore from '@/stores/authStore';

interface RealtimeSubscriptionContextType {
  forceRefresh: (reason?: string) => Promise<void>;
  isRefreshing: boolean;
  lastRefresh: number;
}

const RealtimeSubscriptionContext = createContext<RealtimeSubscriptionContextType | null>(null);

interface RealtimeSubscriptionProviderProps {
  children: ReactNode;
}

export const RealtimeSubscriptionProvider: React.FC<RealtimeSubscriptionProviderProps> = ({ 
  children 
}) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  
  const { 
    forceRefresh, 
    isRefreshing, 
    lastRefresh,
    subscriptionStatus 
  } = useRealtimeSubscription({
    enablePolling: true,
    enableFocusRefresh: true,
    enableNavigationRefresh: true,
    enableVisibilityRefresh: true,
    pollingInterval: 30000, // 30 seconds
  });

  // Log subscription status changes for debugging
  useEffect(() => {
    if (subscriptionStatus) {
      console.log('🔄 Subscription status updated:', {
        status: subscriptionStatus.subscription_status,
        trial_expired: subscriptionStatus.trial_expired,
        days_left: subscriptionStatus.trial_days_left,
        subscription_id: subscriptionStatus.subscription_id,
        timestamp: new Date().toISOString()
      });
    }
  }, [subscriptionStatus]);

  // Enhanced refresh on authentication changes
  useEffect(() => {
    if (isAuthenticated) {
      console.log('🔄 User authenticated - refreshing subscription status');
      forceRefresh('authentication');
    }
  }, [isAuthenticated, forceRefresh]);

  // Keyboard shortcut for manual refresh (Ctrl+Shift+R)
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.ctrlKey && event.shiftKey && event.key === 'R') {
        event.preventDefault();
        console.log('🔄 Manual subscription refresh triggered via keyboard');
        forceRefresh('keyboard shortcut');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [forceRefresh]);

  // Enhanced error recovery - refresh on network reconnection
  useEffect(() => {
    const handleOnline = () => {
      if (isAuthenticated) {
        console.log('🔄 Network reconnected - refreshing subscription status');
        forceRefresh('network reconnection');
      }
    };

    window.addEventListener('online', handleOnline);
    return () => window.removeEventListener('online', handleOnline);
  }, [isAuthenticated, forceRefresh]);

  // Storage event listener for cross-tab synchronization
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === 'subscription_updated' && isAuthenticated) {
        console.log('🔄 Subscription update detected from another tab');
        forceRefresh('cross-tab sync');
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [isAuthenticated, forceRefresh]);

  const contextValue: RealtimeSubscriptionContextType = {
    forceRefresh,
    isRefreshing,
    lastRefresh,
  };

  return (
    <RealtimeSubscriptionContext.Provider value={contextValue}>
      {children}
    </RealtimeSubscriptionContext.Provider>
  );
};

// Custom hook to use the RealtimeSubscriptionContext
export const useRealtimeSubscriptionContext = (): RealtimeSubscriptionContextType => {
  const context = useContext(RealtimeSubscriptionContext);
  if (!context) {
    throw new Error('useRealtimeSubscriptionContext must be used within a RealtimeSubscriptionProvider');
  }
  return context;
};

// Utility function to trigger subscription refresh from anywhere in the app
export const triggerSubscriptionRefresh = (reason: string = 'manual') => {
  // Store the refresh trigger in localStorage for cross-component communication
  localStorage.setItem('subscription_updated', Date.now().toString());
  
  // Dispatch a custom event for same-tab communication
  window.dispatchEvent(new CustomEvent('subscription-refresh-requested', { 
    detail: { reason } 
  }));
  
  console.log(`🔄 Subscription refresh triggered: ${reason}`);
};
