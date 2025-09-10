import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { DialogClose } from "@radix-ui/react-dialog";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { useGetSubscriptionStatus, useCreateCustomerPortal, useCancelSubscription, useReactivateSubscription } from "@/controllers/API/queries/subscriptions";
import useAlertStore from "@/stores/alertStore";
import { useSubscriptionStore } from "@/stores/subscriptionStore";

export default function SubscriptionManagement(): JSX.Element {
  const [isLoading, setIsLoading] = useState(false);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);

  const { data: subscriptionStatus, refetch } = useGetSubscriptionStatus();
  const { mutate: createCustomerPortal } = useCreateCustomerPortal();
  const { mutate: cancelSubscription } = useCancelSubscription();
  const { mutate: reactivateSubscription } = useReactivateSubscription();

  // Real-time subscription status updates
  const { startPolling, stopPolling, refreshStatus } = useSubscriptionStore();

  useEffect(() => {
    // Start polling for real-time updates when component mounts
    startPolling();

    // Cleanup polling when component unmounts
    return () => {
      stopPolling();
    };
  }, [startPolling, stopPolling]);

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
          title: "Portalfel",
          list: [error?.response?.data?.detail || "Misslyckades att öppna kundportal"],
        });
      },
    });
  };

  const handleCancelSubscription = () => {
    cancelSubscription(undefined, {
      onSuccess: () => {
        setSuccessData({
          title: "Prenumeration Avbruten",
        });
        // Refresh both query cache and real-time store
        refetch();
        refreshStatus();
      },
      onError: (error) => {
        setErrorData({
          title: "Avbokningsfel",
          list: [error?.response?.data?.detail || "Misslyckades att avbryta prenumeration"],
        });
      },
    });
  };

  const handleReactivateSubscription = () => {
    reactivateSubscription(undefined, {
      onSuccess: () => {
        setSuccessData({
          title: "Prenumeration Återaktiverad",
          list: ["Din prenumeration är nu aktiv igen!"],
        });
        // Refresh both query cache and real-time store
        refetch();
        refreshStatus();
      },
      onError: (error) => {
        setErrorData({
          title: "Återaktiveringsfel",
          list: [error?.response?.data?.detail || "Misslyckades att återaktivera prenumeration"],
        });
      },
    });
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-green-500 text-white">Aktiv</Badge>;
      case "trial":
        return <Badge className="bg-blue-500 text-white">Gratis provperiod</Badge>;
      case "admin":
        return <Badge className="bg-purple-500 text-white">Administratör</Badge>;
      case "canceled":
        return <Badge variant="secondary">Avbruten</Badge>;
      case "past_due":
        return <Badge className="bg-yellow-500 text-white">Förfallen</Badge>;
      case "expired":
        return <Badge className="bg-red-500 text-white">Utgången</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Ej tillgänglig";
    return new Date(dateString).toLocaleDateString();
  };

  if (!subscriptionStatus) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ForwardedIconComponent name="CreditCard" className="h-5 w-5" />
            Prenumeration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Laddar prenumerationsinformation...</p>
        </CardContent>
      </Card>
    );
  }

  const isOnTrial = subscriptionStatus.subscription_status === "trial";
  const isSubscribed = subscriptionStatus.subscription_status === "active";
  const isCanceled = subscriptionStatus.subscription_status === "canceled";
  const isAdmin = subscriptionStatus.subscription_status === "admin";
  const trialExpired = subscriptionStatus.trial_expired;

  // Don't show subscription management for admin users
  if (isAdmin) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ForwardedIconComponent name="Shield" className="h-5 w-5" />
            Administratörskonto
          </CardTitle>
          <CardDescription>
            Du har full administrativ åtkomst till Axie Studio
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <ForwardedIconComponent name="Crown" className="h-5 w-5 text-blue-500" />
            <div>
              <h4 className="font-medium text-blue-900 dark:text-blue-100">
                Administratörsåtkomst
              </h4>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                Du har obegränsad åtkomst till alla Axie Studio-funktioner som administratör.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ForwardedIconComponent name="CreditCard" className="h-5 w-5" />
          Prenumerationshantering
        </CardTitle>
        <CardDescription>
          Hantera din Axie Studio-prenumeration och fakturering
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Current Status */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-medium">Nuvarande Plan</h3>
            <p className="text-sm text-muted-foreground">
              {isSubscribed ? "Pro-prenumeration" :
               isCanceled ? "Avbruten prenumeration (aktiv till periodens slut)" :
               isOnTrial ? "Gratis Provperiod" : "Ingen Aktiv Plan"}
            </p>
            {isCanceled && subscriptionStatus.subscription_end && (
              <p className="text-xs text-orange-600 mt-1">
                Åtkomst till: {formatDate(subscriptionStatus.subscription_end)}
              </p>
            )}
            {isSubscribed && subscriptionStatus.subscription_end && (
              <p className="text-xs text-green-600 mt-1">
                Nästa fakturering: {formatDate(subscriptionStatus.subscription_end)}
              </p>
            )}
          </div>
          {getStatusBadge(subscriptionStatus.subscription_status)}
        </div>

        {/* Professional Subscription Information */}
        {isSubscribed && (
          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
            <div className="flex items-start gap-3">
              <ForwardedIconComponent name="CheckCircle" className="h-5 w-5 text-green-500 mt-0.5" />
              <div className="flex-1">
                <h4 className="font-medium text-green-900 dark:text-green-100">
                  Pro-prenumeration Aktiv
                </h4>
                <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                  Du har full åtkomst till alla Axie Studio Pro-funktioner.
                </p>
                <div className="mt-3 grid grid-cols-2 gap-4 text-xs">
                  {subscriptionStatus.subscription_id && (
                    <div>
                      <span className="font-medium text-green-800 dark:text-green-200">Prenumerations-ID:</span>
                      <p className="text-green-600 dark:text-green-400 font-mono">
                        {subscriptionStatus.subscription_id.substring(0, 12)}...
                      </p>
                    </div>
                  )}
                  {subscriptionStatus.subscription_start && (
                    <div>
                      <span className="font-medium text-green-800 dark:text-green-200">Startdatum:</span>
                      <p className="text-green-600 dark:text-green-400">
                        {formatDate(subscriptionStatus.subscription_start)}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Trial Information - ENTERPRISE UX (SVENSKA) */}
        {isOnTrial && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div className="flex items-start gap-3">
              <ForwardedIconComponent name="Crown" className="h-5 w-5 text-blue-500 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-900 dark:text-blue-100">
                  Gratis Provperiod Aktiv
                </h4>
                <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                  {trialExpired
                    ? "Din provperiod har gått ut. Prenumerera för att fortsätta använda Axie Studio."
                    : `Du har ${subscriptionStatus.trial_days_left} dagar kvar av din gratis provperiod.`
                  }
                </p>
                {!trialExpired && (
                  <>
                    <p className="text-xs text-blue-600 dark:text-blue-400 mt-2">
                      Provperiod slutar: {formatDate(subscriptionStatus.trial_end)}
                    </p>
                    <div className="mt-3 p-3 bg-green-50 dark:bg-green-900/20 rounded border border-green-200 dark:border-green-800">
                      <p className="text-xs text-green-700 dark:text-green-300 font-medium">
                        💡 Uppgradera nu för omedelbar Pro-åtkomst!
                      </p>
                      <p className="text-xs text-green-600 dark:text-green-400 mt-1">
                        Få full åtkomst till alla Pro-funktioner direkt efter betalning.
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Expired Trial Warning */}
        {trialExpired && !isSubscribed && !isCanceled && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
            <div className="flex items-start gap-3">
              <ForwardedIconComponent name="AlertTriangle" className="h-5 w-5 text-red-500 mt-0.5" />
              <div>
                <h4 className="font-medium text-red-900 dark:text-red-100">
                  Provperiod Utgången
                </h4>
                <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                  Din gratis provperiod har slutat. Prenumerera för att fortsätta använda Axie Studio.
                </p>
                <Button 
                  size="sm" 
                  className="mt-3"
                  onClick={() => window.location.href = "/pricing"}
                >
                  Visa Priser
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Subscription Details */}
        {isSubscribed && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <ForwardedIconComponent name="Calendar" className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm">
                Nästa fakturering: {formatDate(subscriptionStatus.subscription_end)}
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
              <ForwardedIconComponent name="Crown" className="h-4 w-4 mr-2" />
              Uppgradera till Pro
            </Button>
          )}
          
          {trialExpired && (
            <Button 
              onClick={() => window.location.href = "/pricing"}
              className="flex-1"
            >
              Prenumerera Nu
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
              {isLoading ? "Öppnar..." : "Hantera Fakturering"}
            </Button>
          )}

          {isSubscribed && (
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="destructive" size="sm">
                  Avbryt Prenumeration
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Avbryt Prenumeration</DialogTitle>
                  <DialogDescription>
                    Är du säker på att du vill avbryta din prenumeration? Du kommer att förlora åtkomst till Pro-funktioner i slutet av din nuvarande faktureringsperiod.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <DialogClose asChild>
                    <Button variant="outline">Behåll Prenumeration</Button>
                  </DialogClose>
                  <DialogClose asChild>
                    <Button variant="destructive" onClick={handleCancelSubscription}>
                      Avbryt Prenumeration
                    </Button>
                  </DialogClose>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          )}

          {isCanceled && (
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="default" size="sm" className="bg-green-600 hover:bg-green-700">
                  <ForwardedIconComponent name="RotateCcw" className="h-4 w-4 mr-2" />
                  Återaktivera Prenumeration
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Återaktivera Prenumeration</DialogTitle>
                  <DialogDescription>
                    Vill du återaktivera din prenumeration? Din prenumeration kommer att fortsätta och du behåller åtkomst till alla Pro-funktioner.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <DialogClose asChild>
                    <Button variant="outline">Avbryt</Button>
                  </DialogClose>
                  <DialogClose asChild>
                    <Button variant="default" onClick={handleReactivateSubscription} className="bg-green-600 hover:bg-green-700">
                      <ForwardedIconComponent name="CheckCircle" className="h-4 w-4 mr-2" />
                      Återaktivera Nu
                    </Button>
                  </DialogClose>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
