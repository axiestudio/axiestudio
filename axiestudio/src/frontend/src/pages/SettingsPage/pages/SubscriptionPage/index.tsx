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
          title: "Prenumeration avbruten",
        });
        refetch();
      },
      onError: (error) => {
        setErrorData({
          title: "Avbokningsfel",
          list: [error?.response?.data?.detail || "Misslyckades att avbryta prenumeration"],
        });
      },
    });
  };

  if (!subscriptionStatus) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <div className="text-center">
          <ForwardedIconComponent name="Loader2" className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Laddar prenumerationsstatus...</p>
        </div>
      </div>
    );
  }

  const isSubscribed = subscriptionStatus.subscription_status === "active";
  const isOnTrial = subscriptionStatus.subscription_status === "trial";
  const isAdmin = subscriptionStatus.subscription_status === "admin";
  const trialExpired = subscriptionStatus.trial_expired;

  // Show admin view for superusers
  if (isAdmin) {
    return (
      <div className="flex h-full w-full flex-col gap-6 overflow-x-hidden">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tight">Prenumeration</h2>
          <p className="text-muted-foreground">
            Administratörskontoinställningar
          </p>
        </div>

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
                  Som administratör har du obegränsad åtkomst till alla Axie Studio-funktioner utan några prenumerationskrav.
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
        return <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">Aktiv</Badge>;
      case "trial":
        return trialExpired
          ? <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">Provperiod utgången</Badge>
          : <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">Gratis provperiod</Badge>;
      case "admin":
        return <Badge className="bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300">Administratör</Badge>;
      case "canceled":
        return <Badge className="bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300">Avbruten</Badge>;
      default:
        return <Badge className="bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300">Okänt</Badge>;
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Ej tillgänglig";
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="flex h-full w-full flex-col gap-6 overflow-x-hidden">
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold tracking-tight">Prenumerationshantering</h2>
        <p className="text-muted-foreground">
          Hantera din Axie Studio-prenumeration och faktureringsinställningar.
        </p>
      </div>

      <div className="grid gap-6">
        {/* Current Plan Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ForwardedIconComponent name="CreditCard" className="h-5 w-5" />
              Nuvarande plan
            </CardTitle>
            <CardDescription>
              Din nuvarande prenumerationsstatus och plandetaljer
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Status Overview */}
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium">Planstatus</h3>
                <p className="text-sm text-muted-foreground">
                  {isSubscribed ? "Pro-prenumeration" : isOnTrial ? "Gratis provperiod" : "Ingen aktiv plan"}
                </p>
              </div>
              {getStatusBadge(subscriptionStatus.subscription_status)}
            </div>

            {/* Trial Information */}
            {isOnTrial && (
              <div className="space-y-2">
                <h3 className="font-medium">Provperiodsdetaljer</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Provperiodsstart:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.trial_start)}</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Provperiodsslut:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.trial_end)}</p>
                  </div>
                </div>
                {!trialExpired && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-blue-700 dark:text-blue-300">
                      <ForwardedIconComponent name="Clock" className="h-4 w-4 inline mr-1" />
                      {subscriptionStatus.trial_days_left} dagar kvar i din gratis provperiod
                    </p>
                  </div>
                )}
                {trialExpired && (
                  <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <p className="text-sm text-red-700 dark:text-red-300">
                      <ForwardedIconComponent name="AlertTriangle" className="h-4 w-4 inline mr-1" />
                      Din gratis provperiod har avslutat. Prenumerera för att fortsätta använda Axie Studio.
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Subscription Information */}
            {isSubscribed && (
              <div className="space-y-2">
                <h3 className="font-medium">Prenumerationsdetaljer</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Prenumerationsstart:</span>
                    <p className="font-medium">{formatDate(subscriptionStatus.subscription_start)}</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Nästa fakturering:</span>
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
              Prenumerationsåtgärder
            </CardTitle>
            <CardDescription>
              Hantera dina prenumerations- och faktureringsinställningar
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
                  Uppgradera till Pro
                </Button>
              )}
              
              {trialExpired && (
                <Button 
                  onClick={() => window.location.href = "/pricing"}
                  className="flex-1"
                >
                  <ForwardedIconComponent name="Zap" className="h-4 w-4 mr-2" />
                  Prenumerera nu
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
                  {isLoading ? "Öppnar..." : "Hantera fakturering"}
                </Button>
              )}

              {isSubscribed && (
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="destructive" className="flex-1">
                      <ForwardedIconComponent name="X" className="h-4 w-4 mr-2" />
                      Avbryt prenumeration
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Avbryt prenumeration</DialogTitle>
                      <DialogDescription>
                        Är du säker på att du vill avbryta din prenumeration? Du kommer att förlora åtkomst till Pro-funktioner i slutet av din nuvarande faktureringsperiod.
                      </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                      <DialogClose asChild>
                        <Button variant="outline">Behåll prenumeration</Button>
                      </DialogClose>
                      <DialogClose asChild>
                        <Button variant="destructive" onClick={handleCancelSubscription}>
                          Ja, avbryt
                        </Button>
                      </DialogClose>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              )}
            </div>

            {/* Help Text */}
            <div className="text-sm text-muted-foreground space-y-1">
              <p>• Avbryt när som helst utan dolda avgifter</p>
              <p>• Åtkomst fortsätter till slutet av din faktureringsperiod</p>
              <p>• Alla dina data och flöden bevaras</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
