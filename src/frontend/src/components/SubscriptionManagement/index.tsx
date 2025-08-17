import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { Calendar, CreditCard, Crown, ExternalLink, AlertTriangle } from "lucide-react";
import { useGetSubscriptionStatus, useCreateCustomerPortal, useCancelSubscription } from "@/controllers/API/queries/subscriptions";
import useAlertStore from "@/stores/alertStore";

export default function SubscriptionManagement(): JSX.Element {
  const [isLoading, setIsLoading] = useState(false);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  
  const { data: subscriptionStatus, refetch } = useGetSubscriptionStatus();
  const { mutate: createCustomerPortal } = useCreateCustomerPortal();
  const { mutate: cancelSubscription } = useCancelSubscription();

  const handleManageSubscription = () => {
    setIsLoading(true);
    
    createCustomerPortal(undefined, {
      onSuccess: (data) => {
        window.open(data.portal_url, '_blank');
        setIsLoading(false);
      },
      onError: (error) => {
        setIsLoading(false);
        setErrorData({
          title: "Portal Error",
          list: [error?.response?.data?.detail || "Failed to open customer portal"],
        });
      },
    });
  };

  const handleCancelSubscription = () => {
    cancelSubscription(undefined, {
      onSuccess: () => {
        setSuccessData({
          title: "Subscription Cancelled",
        });
        refetch();
      },
      onError: (error) => {
        setErrorData({
          title: "Cancellation Error",
          list: [error?.response?.data?.detail || "Failed to cancel subscription"],
        });
      },
    });
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-green-500 text-white">Active</Badge>;
      case "trial":
        return <Badge className="bg-blue-500 text-white">Free Trial</Badge>;
      case "canceled":
        return <Badge variant="secondary">Cancelled</Badge>;
      case "past_due":
        return <Badge className="bg-yellow-500 text-white">Past Due</Badge>;
      case "expired":
        return <Badge className="bg-red-500 text-white">Expired</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString();
  };

  if (!subscriptionStatus) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CreditCard className="h-5 w-5" />
            Subscription
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Loading subscription information...</p>
        </CardContent>
      </Card>
    );
  }

  const isOnTrial = subscriptionStatus.subscription_status === "trial";
  const isSubscribed = subscriptionStatus.subscription_status === "active";
  const trialExpired = subscriptionStatus.trial_expired;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CreditCard className="h-5 w-5" />
          Subscription Management
        </CardTitle>
        <CardDescription>
          Manage your Axie Studio subscription and billing
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Current Status */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-medium">Current Plan</h3>
            <p className="text-sm text-muted-foreground">
              {isSubscribed ? "Pro Subscription" : isOnTrial ? "Free Trial" : "No Active Plan"}
            </p>
          </div>
          {getStatusBadge(subscriptionStatus.subscription_status)}
        </div>

        {/* Trial Information */}
        {isOnTrial && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Crown className="h-5 w-5 text-blue-500 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-900 dark:text-blue-100">
                  Free Trial Active
                </h4>
                <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                  {trialExpired 
                    ? "Your trial has expired. Subscribe to continue using Axie Studio."
                    : `You have ${subscriptionStatus.trial_days_left} days left in your free trial.`
                  }
                </p>
                {!trialExpired && (
                  <p className="text-xs text-blue-600 dark:text-blue-400 mt-2">
                    Trial ends: {formatDate(subscriptionStatus.trial_end)}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Expired Trial Warning */}
        {trialExpired && !isSubscribed && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
            <div className="flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-red-500 mt-0.5" />
              <div>
                <h4 className="font-medium text-red-900 dark:text-red-100">
                  Trial Expired
                </h4>
                <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                  Your free trial has ended. Subscribe to continue using Axie Studio.
                </p>
                <Button 
                  size="sm" 
                  className="mt-3"
                  onClick={() => window.location.href = "/pricing"}
                >
                  View Pricing
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Subscription Details */}
        {isSubscribed && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm">
                Next billing: {formatDate(subscriptionStatus.subscription_end)}
              </span>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3 pt-4 border-t">
          {!isSubscribed && !trialExpired && (
            <Button 
              onClick={() => window.location.href = "/pricing"}
              className="flex-1"
            >
              <Crown className="h-4 w-4 mr-2" />
              Upgrade to Pro
            </Button>
          )}
          
          {trialExpired && (
            <Button 
              onClick={() => window.location.href = "/pricing"}
              className="flex-1"
            >
              Subscribe Now
            </Button>
          )}

          {subscriptionStatus.has_stripe_customer && (
            <Button 
              variant="outline" 
              onClick={handleManageSubscription}
              disabled={isLoading}
              className="flex-1"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              {isLoading ? "Opening..." : "Manage Billing"}
            </Button>
          )}

          {isSubscribed && (
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive" size="sm">
                  Cancel Subscription
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Cancel Subscription</AlertDialogTitle>
                  <AlertDialogDescription>
                    Are you sure you want to cancel your subscription? You'll lose access to Pro features at the end of your current billing period.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Keep Subscription</AlertDialogCancel>
                  <AlertDialogAction onClick={handleCancelSubscription}>
                    Cancel Subscription
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
