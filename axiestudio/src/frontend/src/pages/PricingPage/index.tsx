import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check, Crown, Zap } from "lucide-react";
import { useCreateCheckout, useGetSubscriptionStatus } from "@/controllers/API/queries/subscriptions";
import useAlertStore from "@/stores/alertStore";

export default function PricingPage(): JSX.Element {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const setErrorData = useAlertStore((state) => state.setErrorData);
  
  const { mutate: createCheckout } = useCreateCheckout();
  const { data: subscriptionStatus } = useGetSubscriptionStatus();

  const handleSubscribe = () => {
    setIsLoading(true);
    
    const successUrl = `${window.location.origin}/subscription-success`;
    const cancelUrl = `${window.location.origin}/pricing`;
    
    createCheckout(
      { success_url: successUrl, cancel_url: cancelUrl },
      {
        onSuccess: (data) => {
          window.location.href = data.checkout_url;
        },
        onError: (error) => {
          setIsLoading(false);
          setErrorData({
            title: "Prenumerationsfel",
            list: [error?.response?.data?.detail || "Misslyckades att skapa checkout-session"],
          });
        },
      }
    );
  };

  const handleContinueToApp = () => {
    // Smart redirect: Check if user came from signup, redirect to flows
    const urlParams = new URLSearchParams(window.location.search);
    const fromSignup = urlParams.get('from') === 'signup';

    if (fromSignup) {
      navigate("/flows");
    } else {
      navigate("/");
    }
  };

  const isOnTrial = subscriptionStatus?.subscription_status === "trial";
  const isSubscribed = subscriptionStatus?.subscription_status === "active";
  const trialExpired = subscriptionStatus?.trial_expired;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Välj Din Plan
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Börja med en 7-dagars gratis provperiod, fortsätt sedan med vår Pro-plan
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          {/* Free Trial Card */}
          <Card className="relative border-2 border-gray-200 dark:border-gray-700">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Gratis Provperiod</CardTitle>
                <Zap className="h-6 w-6 text-blue-500" />
              </div>
              <CardDescription>Perfekt för att komma igång</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-4">
                $0
                <span className="text-lg font-normal text-gray-500"> / 7 dagar</span>
              </div>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Full åtkomst till alla funktioner</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Obegränsade flöden</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Community-support</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Inget kreditkort krävs</span>
                </li>
              </ul>
              {isOnTrial && !trialExpired && (
                <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <p className="text-sm text-blue-700 dark:text-blue-300">
                    Du har {subscriptionStatus?.trial_days_left} dagar kvar av din provperiod
                  </p>
                </div>
              )}
            </CardContent>
            <CardFooter>
              {isOnTrial && !trialExpired ? (
                <Button
                  onClick={handleContinueToApp}
                  className="w-full"
                  variant="outline"
                >
                  Fortsätt till App
                </Button>
              ) : !subscriptionStatus ? (
                <Button
                  onClick={handleContinueToApp}
                  className="w-full"
                  variant="outline"
                >
                  Starta Gratis Provperiod
                </Button>
              ) : (
                <Button
                  disabled
                  className="w-full"
                  variant="outline"
                >
                  {trialExpired ? "Provperiod Utgången" : "Nuvarande Plan"}
                </Button>
              )}
            </CardFooter>
          </Card>

          {/* Pro Plan Card */}
          <Card className="relative border-2 border-blue-500 dark:border-blue-400 shadow-lg">
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <Badge className="bg-blue-500 text-white px-3 py-1">
                <Crown className="h-3 w-3 mr-1" />
                Rekommenderad
              </Badge>
            </div>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Pro-prenumeration</CardTitle>
                <Crown className="h-6 w-6 text-blue-500" />
              </div>
              <CardDescription>För seriös AI-arbetsflödesautomation</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-4">
                $45
                <span className="text-lg font-normal text-gray-500"> / månad</span>
              </div>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Allt i Gratis Provperiod</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Obegränsad användning</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Prioriterad support</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Avancerade integrationer</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Teamsamarbete</span>
                </li>
              </ul>
              {trialExpired && (
                <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <p className="text-sm text-red-700 dark:text-red-300">
                    Din provperiod har gått ut. Prenumerera för att fortsätta använda Axie Studio.
                  </p>
                </div>
              )}
            </CardContent>
            <CardFooter>
              {isSubscribed ? (
                <Button disabled className="w-full">
                  Nuvarande Plan
                </Button>
              ) : (
                <Button 
                  onClick={handleSubscribe} 
                  disabled={isLoading}
                  className="w-full bg-blue-500 hover:bg-blue-600"
                >
                  {isLoading ? "Bearbetar..." : "Starta Prenumeration"}
                </Button>
              )}
            </CardFooter>
          </Card>
        </div>

        <div className="text-center mt-8">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Avbryt när som helst. Inga dolda avgifter.
            {!isSubscribed && !trialExpired && (
              <span className="block mt-1">
                Din prenumeration startar efter att din 7-dagars gratis provperiod slutar.
              </span>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
