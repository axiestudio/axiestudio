/**
 * Real-time subscription verification hook
 * Ensures users always have the latest subscription status across all app interactions
 */

import { useEffect, useCallback, useRef } from 'react';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { useGetSubscriptionStatus } from '@/controllers/API/queries/subscriptions';
import useAuthStore from '@/stores/authStore';

interface UseRealtimeSubscriptionOptions {
  enablePolling?: boolean;
  enableFocusRefresh?: boolean;
  enableNavigationRefresh?: boolean;
  enableVisibilityRefresh?: boolean;
  pollingInterval?: number;
}

export const useRealtimeSubscription = (options: UseRealtimeSubscriptionOptions = {}) => {
  const {
    enablePolling = true,
    enableFocusRefresh = true,
    enableNavigationRefresh = true,
    enableVisibilityRefresh = true,
    pollingInterval = 30000, // 30 seconds
  } = options;

  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const { 
    refreshStatus, 
    startPolling, 
    stopPolling, 
    startFastPolling,
    subscriptionStatus 
  } = useSubscriptionStore();
  
  const { refetch } = useGetSubscriptionStatus();
  const lastRefreshRef = useRef<number>(0);
  const isRefreshingRef = useRef<boolean>(false);

  // Debounced refresh function to prevent excessive API calls
  const debouncedRefresh = useCallback(async (reason: string) => {
    const now = Date.now();
    const timeSinceLastRefresh = now - lastRefreshRef.current;
    
    // Prevent refresh if less than 2 seconds since last refresh
    if (timeSinceLastRefresh < 2000 || isRefreshingRef.current) {
      console.log(`🔄 Subscription refresh skipped (${reason}) - too recent or already refreshing`);
      return;
    }

    if (!isAuthenticated) {
      console.log(`🔄 Subscription refresh skipped (${reason}) - not authenticated`);
      return;
    }

    try {
      isRefreshingRef.current = true;
      lastRefreshRef.current = now;
      
      console.log(`🔄 Refreshing subscription status (${reason})`);
      
      // Use both store refresh (with real-time) and query refetch for maximum reliability
      await Promise.all([
        refreshStatus(true), // Use real-time endpoint
        refetch()
      ]);
      
      console.log(`✅ Subscription status refreshed successfully (${reason})`);
    } catch (error) {
      console.error(`❌ Failed to refresh subscription status (${reason}):`, error);
    } finally {
      isRefreshingRef.current = false;
    }
  }, [isAuthenticated, refreshStatus, refetch]);

  // 1. PAGE FOCUS REFRESH - When user returns to the app
  useEffect(() => {
    if (!enableFocusRefresh || !isAuthenticated) return;

    const handleFocus = () => debouncedRefresh('page focus');
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        debouncedRefresh('visibility change');
      }
    };

    window.addEventListener('focus', handleFocus);
    if (enableVisibilityRefresh) {
      document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    return () => {
      window.removeEventListener('focus', handleFocus);
      if (enableVisibilityRefresh) {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
      }
    };
  }, [enableFocusRefresh, enableVisibilityRefresh, isAuthenticated, debouncedRefresh]);

  // 2. NAVIGATION REFRESH - When user navigates between pages
  useEffect(() => {
    if (!enableNavigationRefresh || !isAuthenticated) return;

    const handlePopState = () => debouncedRefresh('navigation');
    
    window.addEventListener('popstate', handlePopState);
    
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, [enableNavigationRefresh, isAuthenticated, debouncedRefresh]);

  // 3. POLLING MANAGEMENT - Start/stop polling based on authentication
  useEffect(() => {
    if (!isAuthenticated) {
      stopPolling();
      return;
    }

    if (enablePolling) {
      // Initial refresh when authentication changes
      debouncedRefresh('authentication change');
      
      // Start polling
      startPolling();
    }

    return () => {
      if (enablePolling) {
        stopPolling();
      }
    };
  }, [isAuthenticated, enablePolling, startPolling, stopPolling, debouncedRefresh]);

  // 4. PAYMENT SUCCESS DETECTION - Enhanced fast polling for payment scenarios
  useEffect(() => {
    if (!isAuthenticated) return;

    // Check if we're on a payment success page or have payment-related URL params
    const urlParams = new URLSearchParams(window.location.search);
    const hasPaymentParams = urlParams.has('session_id') || 
                            window.location.pathname.includes('subscription-success') ||
                            window.location.pathname.includes('pricing');

    if (hasPaymentParams) {
      console.log('🚀 Payment context detected - starting fast polling');
      startFastPolling();
      
      // Also do an immediate refresh
      debouncedRefresh('payment context');
    }
  }, [isAuthenticated, startFastPolling, debouncedRefresh]);

  // 5. SUBSCRIPTION STATUS CHANGE DETECTION
  const previousStatusRef = useRef<string | null>(null);
  useEffect(() => {
    if (subscriptionStatus?.subscription_status) {
      const currentStatus = subscriptionStatus.subscription_status;
      
      if (previousStatusRef.current && previousStatusRef.current !== currentStatus) {
        console.log(`🔄 Subscription status changed: ${previousStatusRef.current} → ${currentStatus}`);
        
        // If status changed to active, do an additional refresh to ensure all data is current
        if (currentStatus === 'active') {
          setTimeout(() => debouncedRefresh('status change to active'), 1000);
        }
      }
      
      previousStatusRef.current = currentStatus;
    }
  }, [subscriptionStatus?.subscription_status, debouncedRefresh]);

  // Manual refresh function for components to use
  const forceRefresh = useCallback((reason: string = 'manual') => {
    return debouncedRefresh(reason);
  }, [debouncedRefresh]);

  return {
    subscriptionStatus,
    forceRefresh,
    isRefreshing: isRefreshingRef.current,
    lastRefresh: lastRefreshRef.current,
  };
};
