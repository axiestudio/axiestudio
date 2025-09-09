import { useEffect, useState } from "react";
import { CustomNavigate } from "@/customization/components/custom-navigate";
import { LoadingPage } from "@/pages/LoadingPage";
import { useGetSubscriptionStatus } from "@/controllers/API/queries/subscriptions";
import useAuthStore from "@/stores/authStore";
import useAlertStore from "@/stores/alertStore";
import { useRealtimeSubscriptionContext } from "@/components/providers/RealtimeSubscriptionProvider";

interface SubscriptionGuardProps {
  children: React.ReactNode;
}

export const SubscriptionGuard = ({ children }: SubscriptionGuardProps) => {
  const [isChecking, setIsChecking] = useState(true);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isAdmin = useAuthStore((state) => state.isAdmin);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  const { data: subscriptionStatus, isLoading, error, refetch } = useGetSubscriptionStatus();
  const { forceRefresh } = useRealtimeSubscriptionContext();

  useEffect(() => {
    // If not authenticated, let auth guard handle it
    if (!isAuthenticated) {
      setIsChecking(false);
      return;
    }

    // Admin users bypass subscription checks
    if (isAdmin) {
      setIsChecking(false);
      return;
    }

    // CRITICAL: Force refresh subscription status when guard is mounted
    // This ensures we always have the latest subscription data
    if (isAuthenticated && !isAdmin) {
      forceRefresh('subscription guard mounted').catch(console.error);
    }

    // If we have subscription data or error, stop checking
    if (subscriptionStatus || error) {
      setIsChecking(false);
    }
  }, [isAuthenticated, isAdmin, subscriptionStatus, error, forceRefresh]);

  // Not authenticated - let auth guard handle
  if (!isAuthenticated) {
    return <>{children}</>;
  }

  // Admin users always have access
  if (isAdmin) {
    return <>{children}</>;
  }

  // Still loading subscription status
  if (isChecking || isLoading) {
    return <LoadingPage />;
  }

  // Error loading subscription status - allow access but log error
  if (error) {
    console.error("Failed to load subscription status:", error);
    return <>{children}</>;
  }

  // STRICT SUBSCRIPTION ENFORCEMENT
  if (subscriptionStatus) {
    const isSubscribed = subscriptionStatus.subscription_status === "active";
    const isOnTrial = subscriptionStatus.subscription_status === "trial";
    const isCanceled = subscriptionStatus.subscription_status === "canceled";
    const trialExpired = subscriptionStatus.trial_expired;
    // FIXED: Include "canceled" as a valid status since canceled subscriptions can still be active until period end
    const hasValidStatus = ["active", "trial", "admin", "canceled"].includes(subscriptionStatus.subscription_status);

    // CRITICAL: Never block active subscribers
    if (isSubscribed) {
      // Active subscribers always have access, regardless of trial status
      return <>{children}</>;
    }

    // Block access for ANY of these conditions:
    const shouldBlock = (
      // Trial expired and no active subscription and no valid canceled subscription
      (trialExpired && !isSubscribed && !isCanceled) ||
      // Invalid subscription status
      (!hasValidStatus) ||
      // No subscription status at all
      (!subscriptionStatus.subscription_status) ||
      // Trial user with no days left
      (isOnTrial && subscriptionStatus.trial_days_left !== null && subscriptionStatus.trial_days_left <= 0)
    );

    if (shouldBlock) {
      console.warn("🚫 BLOCKING ACCESS - Subscription required:", {
        status: subscriptionStatus.subscription_status,
        trialExpired,
        daysLeft: subscriptionStatus.trial_days_left
      });

      // Show error message
      setErrorData({
        title: "Prenumeration krävs",
        list: [
          trialExpired 
            ? "Din kostnadsfria provperiod har löpt ut. Vänligen prenumerera för att fortsätta använda Axie Studio."
            : "En giltig prenumeration krävs för att komma åt Axie Studio."
        ]
      });

      // Redirect to pricing page
      return <CustomNavigate to="/pricing" replace />;
    }
  }

  // All checks passed - render children
  return <>{children}</>;
};
