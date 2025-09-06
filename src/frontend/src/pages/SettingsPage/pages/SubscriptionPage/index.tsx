import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { DialogClose } from "@radix-ui/react-dialog";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { useGetSubscriptionStatus, useCreateCustomerPortal, useCancelSubscription } from "@/controllers/API/queries/subscriptions";
import useAlertStore from "@/stores/alertStore";

export default function SubscriptionPage(): JSX.Element {
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

  if (!subscriptionStatus) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <div className="text-center">
          <ForwardedIconComponent name="Loader2" className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading subscription status...</p>
        </div>
      </div>
    );
  }

  const isSubscribed = subscriptionStatus.subscription_status === "active";
  const isOnTrial = subscriptionStatus.subscription_status === "trial";
  const isCanceled = subscriptionStatus.subscription_status === "canceled";
  const isAdmin = subscriptionStatus.subscription_status === "admin";
  const trialExpired = subscriptionStatus.trial_expired;

  // Show admin view for superusers
  if (isAdmin) {
    return (
      <div className="flex h-full w-full flex-col gap-6 overflow-x-hidden">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tight">Subscription</h2>
          <p className="text-muted-foreground">
            Administrator account settings
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ForwardedIconComponent name="Shield" className="h-5 w-5" />
              Administrator Account
            </CardTitle>
            <CardDescription>
              You have full administrative access to Axie Studio
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <ForwardedIconComponent name="Crown" className="h-5 w-5 text-blue-500" />
              <div>
                <h4 className="font-medium text-blue-900 dark:text-blue-100">
                  Administrator Access
                </h4>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  As an administrator, you have unlimited access to all Axie Studio features without any subscription requirements.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">Active</Badge>;
      case "trial":
        return trialExpired
          ? <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">Trial Expired</Badge>
          : <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">Free Trial</Badge>;
      case "admin":
        return <Badge className="bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300">Administrator</Badge>;
      case "canceled":
        return <Badge className="bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300">Cancelled</Badge>;
      default:
        return <Badge className="bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300">Unknown</Badge>;
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="flex h-full w-full flex-col gap-6 overflow-x-hidden">
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold tracking-tight">Subscription Management</h2>
        <p className="text-muted-foreground">
          Manage your Axie Studio subscription and billing preferences.
        </p>
      </div>

      <div className="grid gap-6">
        {/* Current Plan Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ForwardedIconComponent name="CreditCard" className="h-5 w-5" />
              Current Plan
            </CardTitle>
            <CardDescription>
              Your current subscription status and plan details
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Status Overview */}
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium">Plan Status</h3>
                <p className="text-sm text-muted-foreground">
                  {isSubscribed ? "Pro Subscription" : isOnTrial ? "Free Trial" : "No Active Plan"}
                </p>
              </div>
              {getStatusBadge(subscriptionStatus.subscription_status)}
            </div>

            {/* Trial Information */}
            {isOnTrial && (
              <div className="space-y-2">
                <h3 className="font-medium">Trial Details</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Trial Start:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.trial_start)}</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Trial End:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.trial_end)}</p>
                  </div>
                </div>
                {!trialExpired && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-blue-700 dark:text-blue-300">
                      <ForwardedIconComponent name="Clock" className="h-4 w-4 inline mr-1" />
                      {subscriptionStatus.trial_days_left} days remaining in your free trial
                    </p>
                  </div>
                )}
                {trialExpired && (
                  <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <p className="text-sm text-red-700 dark:text-red-300">
                      <ForwardedIconComponent name="AlertTriangle" className="h-4 w-4 inline mr-1" />
                      Your free trial has expired. Subscribe to continue using Axie Studio.
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Subscription Information */}
            {isSubscribed && (
              <div className="space-y-2">
                <h3 className="font-medium">Subscription Details</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Subscription Start:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.subscription_start)}</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Next Billing:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.subscription_end)}</p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Actions Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ForwardedIconComponent name="Settings" className="h-5 w-5" />
              Subscription Actions
            </CardTitle>
            <CardDescription>
              Manage your subscription and billing settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col sm:flex-row gap-3">
              {!isSubscribed && !trialExpired && (
                <Button 
                  onClick={() => window.location.href = "/pricing"}
                  className="flex-1"
                >
                  <ForwardedIconComponent name="Crown" className="h-4 w-4 mr-2" />
                  Upgrade to Pro
                </Button>
              )}
              
              {trialExpired && (
                <Button 
                  onClick={() => window.location.href = "/pricing"}
                  className="flex-1"
                >
                  <ForwardedIconComponent name="Zap" className="h-4 w-4 mr-2" />
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
                  <ForwardedIconComponent name="ExternalLink" className="h-4 w-4 mr-2" />
                  {isLoading ? "Opening..." : "Manage Billing"}
                </Button>
              )}

              {isSubscribed && (
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="destructive" className="flex-1">
                      <ForwardedIconComponent name="X" className="h-4 w-4 mr-2" />
                      Cancel Subscription
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Cancel Subscription</DialogTitle>
                      <DialogDescription>
                        Are you sure you want to cancel your subscription? You'll lose access to Pro features at the end of your current billing period.
                      </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                      <DialogClose asChild>
                        <Button variant="outline">Keep Subscription</Button>
                      </DialogClose>
                      <DialogClose asChild>
                        <Button variant="destructive" onClick={handleCancelSubscription}>
                          Yes, Cancel
                        </Button>
                      </DialogClose>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              )}
            </div>

            {/* Help Text */}
            <div className="text-sm text-muted-foreground space-y-1">
              <p>• Cancel anytime with no hidden fees</p>
              <p>• Access continues until the end of your billing period</p>
              <p>• All your data and flows are preserved</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
