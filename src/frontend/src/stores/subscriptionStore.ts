import { create } from 'zustand';
import { subscriptionsApi } from '@/controllers/API/queries/subscriptions';

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
}

let pollingInterval: NodeJS.Timeout | null = null;

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
        console.error('Failed to poll subscription status:', error);
      }
    }, 30000); // 30 seconds
  },

  stopPolling: () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
    set({ isPolling: false });
  },

  refreshStatus: async () => {
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
      console.error('Failed to refresh subscription status:', error);
      throw error;
    }
  },
}));

// Auto-cleanup on page unload
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', () => {
    useSubscriptionStore.getState().stopPolling();
  });
}
