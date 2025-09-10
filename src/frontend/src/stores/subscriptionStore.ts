import { create } from 'zustand';

interface SubscriptionStatus {
  subscription_status: string;
  subscription_id: string | null;
  trial_start: string | null;
  trial_end: string | null;
  trial_expired: boolean;
  trial_days_left: number | null;
  subscription_start: string | null;
  subscription_end: string | null;
  has_stripe_customer: boolean;
  is_superuser?: boolean;
}

interface SubscriptionStore {
  subscriptionStatus: SubscriptionStatus | null;
  isPolling: boolean;
  lastUpdated: Date | null;

  // Actions
  setSubscriptionStatus: (status: SubscriptionStatus) => void;
  startPolling: () => void;
  stopPolling: () => void;
  refreshStatus: () => Promise<void>;
  startFastPolling: () => void; // For immediate post-payment polling
}

let pollingInterval: NodeJS.Timeout | null = null;
let fastPollingInterval: NodeJS.Timeout | null = null;

export const useSubscriptionStore = create<SubscriptionStore>((set, get) => ({
  subscriptionStatus: null,
  isPolling: false,
  lastUpdated: null,

  setSubscriptionStatus: (status: SubscriptionStatus) => {
    set({ 
      subscriptionStatus: status, 
      lastUpdated: new Date() 
    });
  },

  startPolling: () => {
    const { isPolling } = get();
    
    if (isPolling || pollingInterval) {
      return; // Already polling
    }

    set({ isPolling: true });

    // Poll every 30 seconds for subscription status changes
    pollingInterval = setInterval(async () => {
      try {
        const response = await fetch('/api/v1/subscriptions/status', {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (response.ok) {
          const status = await response.json();
          get().setSubscriptionStatus(status);
        }
      } catch (error) {
        // Silent polling failure
      }
    }, 30000); // 30 seconds
  },

  stopPolling: () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
    if (fastPollingInterval) {
      clearInterval(fastPollingInterval);
      fastPollingInterval = null;
    }
    set({ isPolling: false });
  },

  refreshStatus: async (useRealtime: boolean = false) => {
    try {
      const endpoint = useRealtime ? '/api/v1/subscriptions/status/realtime' : '/api/v1/subscriptions/status';

      const response = await fetch(endpoint, {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const status = await response.json();
        get().setSubscriptionStatus(status);

      }
    } catch (error) {
      throw error;
    }
  },

  startFastPolling: () => {
    // CRITICAL FIX: Fast polling for immediate post-payment updates
    // Poll every 3 seconds for the first 2 minutes after payment
    if (fastPollingInterval) {
      clearInterval(fastPollingInterval);
    }

    let pollCount = 0;
    const maxPolls = 40; // 40 polls * 3 seconds = 2 minutes

    fastPollingInterval = setInterval(async () => {
      pollCount++;

      try {
        // Use real-time endpoint for fast polling to get most accurate data
        const response = await fetch('/api/v1/subscriptions/status/realtime', {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const status = await response.json();
          get().setSubscriptionStatus(status);

          // Stop fast polling if subscription becomes active
          if (status.subscription_status === 'active') {
            if (fastPollingInterval) {
              clearInterval(fastPollingInterval);
              fastPollingInterval = null;
            }
            return;
          }
        }
      } catch (error) {
        // Fallback to standard endpoint if real-time fails
        try {
          const fallbackResponse = await fetch('/api/v1/subscriptions/status', {
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (fallbackResponse.ok) {
            const status = await fallbackResponse.json();
            get().setSubscriptionStatus(status);
          }
        } catch (fallbackError) {
          // Silent fallback failure
        }
      }

      // Stop fast polling after max attempts
      if (pollCount >= maxPolls) {
        if (fastPollingInterval) {
          clearInterval(fastPollingInterval);
          fastPollingInterval = null;
        }
      }
    }, 3000); // 3 seconds
  },
}));

// Auto-cleanup on page unload
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', () => {
    useSubscriptionStore.getState().stopPolling();
  });
}
