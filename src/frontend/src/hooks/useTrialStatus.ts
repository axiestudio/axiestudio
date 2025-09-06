import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/controllers/API";
import useAuthStore from "@/stores/authStore";
import { useNavigate } from "react-router-dom";
import useAlertStore from "@/stores/alertStore";

interface TrialStatus {
  user_id: string;
  username: string;
  subscription_status: string;
  is_superuser: boolean;
  status: "trial" | "expired" | "subscribed" | "admin";
  trial_expired: boolean;
  days_left: number;
  should_cleanup: boolean;
  trial_end?: string;
}

export const useTrialStatus = () => {
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const setNoticeData = useAlertStore((state) => state.setNoticeData);
  const [hasShownExpiredWarning, setHasShownExpiredWarning] = useState(false);

  const {
    data: trialStatus,
    error,
    isLoading,
    refetch,
  } = useQuery<TrialStatus>({
    queryKey: ["trial-status"],
    queryFn: async () => {
      const response = await api.get("/api/v1/users/trial-status");
      return response.data;
    },
    enabled: isAuthenticated,
    refetchInterval: 5 * 60 * 1000, // Check every 5 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });

  // Handle expired trial with enhanced UX
  useEffect(() => {
    if (trialStatus && trialStatus.should_cleanup && !hasShownExpiredWarning) {
      setHasShownExpiredWarning(true);

      // Enhanced error message with upgrade benefits
      setErrorData({
        title: "🚨 Trial Expired - Your free trial has expired",
        list: [
          "Your 7-day free trial has ended",
          "Subscribe now to continue using Axie Studio",
          "✨ Get unlimited AI/ML workflows",
          "🚀 Access to advanced components",
          "💬 Priority support included",
          "📊 Export and sharing capabilities"
        ]
      });

      // Redirect to pricing page with context
      setTimeout(() => {
        navigate("/pricing?from=trial-expired&reason=expired");
      }, 4000); // Slightly longer delay to read benefits
    }
  }, [trialStatus, hasShownExpiredWarning, navigate, setErrorData]);

  // Enhanced trial expiration warnings with urgency levels
  useEffect(() => {
    if (trialStatus && trialStatus.status === "trial" && trialStatus.days_left >= 0) {
      const daysLeft = trialStatus.days_left;

      // Different urgency levels based on days remaining
      if (daysLeft === 0) {
        // Last day - critical warning
        setErrorData({
          title: "🚨 Trial Expires Today!",
          list: [
            "Your free trial expires in less than 24 hours",
            "Subscribe now to avoid service interruption",
            "All your projects and data will be preserved"
          ]
        });
      } else if (daysLeft === 1) {
        // 1 day left - urgent warning
        setErrorData({
          title: "⚠️ Trial Expires Tomorrow",
          list: [
            "Only 1 day left in your free trial",
            "Subscribe today to continue seamlessly",
            "Don't lose access to your AI workflows"
          ]
        });
      } else if (daysLeft <= 3) {
        // 2-3 days left - notice
        setNoticeData({
          title: `⏰ Trial Expiring Soon - ${daysLeft} day${daysLeft === 1 ? "" : "s"} remaining. Subscribe now to continue using Axie Studio.`,
          link: "/pricing?from=trial-warning&days=" + daysLeft
        });
      }
    }
  }, [trialStatus, setNoticeData, setErrorData]);

  return {
    trialStatus,
    isLoading,
    error,
    refetch,
    isTrialExpired: trialStatus?.should_cleanup || false,
    isSubscribed: trialStatus?.subscription_status === "active" || false,
    daysLeft: trialStatus?.days_left || 0,
    isSuperuser: trialStatus?.is_superuser || false,
  };
};
