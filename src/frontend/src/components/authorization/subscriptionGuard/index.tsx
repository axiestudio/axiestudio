import { useEffect, useState } from "react";
import { CustomNavigate } from "@/customization/components/custom-navigate";
import { LoadingPage } from "@/pages/LoadingPage";
import { useGetSubscriptionStatus } from "@/controllers/API/queries/subscriptions";
import useAuthStore from "@/stores/authStore";
import useAlertStore from "@/stores/alertStore";

interface SubscriptionGuardProps {
  children: React.ReactNode;
}

export const SubscriptionGuard = ({ children }: SubscriptionGuardProps) => {
  const [isChecking, setIsChecking] = useState(true);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isAdmin = useAuthStore((state) => state.isAdmin);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  
  const { data: subscriptionStatus, isLoading, error } = useGetSubscriptionStatus();

  useEffect(() => {
    if (!isLoading) {
      setIsChecking(false);
    }
  }, [isLoading]);

  // Don't check subscription for unauthenticated users (auth guard will handle)
  if (!isAuthenticated) {
    return children;
  }

  // Admin users bypass subscription checks
  if (isAdmin || subscriptionStatus?.is_superuser) {
    return children;
  }

  // Still loading subscription status
  if (isChecking || isLoading) {
    return <LoadingPage />;
  }

  // Error loading subscription status - allow access but log error
  if (error) {
    console.error("Failed to load subscription status:", error);
    return children;
  }

  // STRICT SUBSCRIPTION ENFORCEMENT
  if (subscriptionStatus) {
    const isSubscribed = subscriptionStatus.subscription_status === "active";
    const isOnTrial = subscriptionStatus.subscription_status === "trial";
    const isCanceled = subscriptionStatus.subscription_status === "canceled";
    const trialExpired = subscriptionStatus.trial_expired;
    // FIXED: Include "canceled" as a valid status since canceled subscriptions can still be active until period end
    const hasValidStatus = ["active", "trial", "admin", "canceled"].includes(subscriptionStatus.subscription_status);

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
        title: "Subscription Required",
        list: [
          trialExpired
            ? "Your free trial has expired. Please subscribe to continue using Axie Studio."
            : "A valid subscription is required to access Axie Studio."
        ]
      });

      // Redirect to pricing page
      return <CustomNavigate to="/pricing" replace />;
    }
  }

  // Allow access for active subscribers or users with active trial
  return children;
};
