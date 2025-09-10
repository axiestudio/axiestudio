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
            title: "Subscription Error",
            list: [error?.response?.data?.detail || "Failed to create checkout session"],
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
  const isCanceled = subscriptionStatus?.subscription_status === "canceled";
  const trialExpired = subscriptionStatus?.trial_expired;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Start with a 7-day free trial, then continue with our Pro plan
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          {/* Free Trial Card */}
          <Card className="relative border-2 border-gray-200 dark:border-gray-700">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Free Trial</CardTitle>
                <Zap className="h-6 w-6 text-blue-500" />
              </div>
              <CardDescription>Perfect for getting started</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-4">
                $0
                <span className="text-lg font-normal text-gray-500"> / 7 days</span>
              </div>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Full access to all features</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Unlimited flows</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Community support</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>No credit card required</span>
                </li>
              </ul>
              {isOnTrial && !trialExpired && (
                <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <p className="text-sm text-blue-700 dark:text-blue-300">
                    You have {subscriptionStatus?.trial_days_left} days left in your trial
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
                  Continue to App
                </Button>
              ) : isCanceled ? (
                <Button
                  onClick={handleContinueToApp}
                  className="w-full"
                  variant="outline"
                >
                  Continue to App
                </Button>
              ) : !subscriptionStatus ? (
                <Button
                  onClick={handleContinueToApp}
                  className="w-full"
                  variant="outline"
                >
                  Start Free Trial
                </Button>
              ) : (
                <Button
                  disabled
                  className="w-full"
                  variant="outline"
                >
                  {trialExpired ? "Trial Expired" : "Current Plan"}
                </Button>
              )}
            </CardFooter>
          </Card>

          {/* Pro Plan Card */}
          <Card className="relative border-2 border-blue-500 dark:border-blue-400 shadow-lg">
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <Badge className="bg-blue-500 text-white px-3 py-1">
                <Crown className="h-3 w-3 mr-1" />
                Recommended
              </Badge>
            </div>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Pro Subscription</CardTitle>
                <Crown className="h-6 w-6 text-blue-500" />
              </div>
              <CardDescription>For serious AI workflow automation</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-4">
                $45
                <span className="text-lg font-normal text-gray-500"> / month</span>
              </div>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Everything in Free Trial</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Unlimited usage</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Priority support</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Advanced integrations</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-4 w-4 text-green-500 mr-2" />
                  <span>Team collaboration</span>
                </li>
              </ul>
              {trialExpired && (
                <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <p className="text-sm text-red-700 dark:text-red-300">
                    Your trial has expired. Subscribe to continue using Axie Studio.
                  </p>
                </div>
              )}
              {isCanceled && (
                <div className="mt-4 p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <p className="text-sm text-orange-700 dark:text-orange-300">
                    Your subscription is canceled but still active until {subscriptionStatus?.subscription_end ? new Date(subscriptionStatus.subscription_end).toLocaleDateString() : 'the end of your billing period'}. You can reactivate anytime!
                  </p>
                </div>
              )}
            </CardContent>
            <CardFooter>
              {isSubscribed ? (
                <Button disabled className="w-full">
                  Current Plan
                </Button>
              ) : isCanceled ? (
                <Button
                  onClick={handleSubscribe}
                  disabled={isLoading}
                  className="w-full bg-green-600 hover:bg-green-700"
                >
                  {isLoading ? "Processing..." : "Reactivate Subscription"}
                </Button>
              ) : (
                <div className="w-full space-y-3">
                  <Button
                    onClick={handleSubscribe}
                    disabled={isLoading}
                    className="w-full bg-blue-500 hover:bg-blue-600"
                  >
                    {isLoading ? "Processing..." : isOnTrial ? "Upgrade Now" : "Start Subscription"}
                  </Button>
                  {isOnTrial && (
                    <div className="text-center p-2 bg-green-50 dark:bg-green-900/20 rounded text-xs">
                      <p className="text-green-700 dark:text-green-300 font-medium">
                        🚀 Upgrade from trial
                      </p>
                      <p className="text-green-600 dark:text-green-400 mt-1">
                        Get immediate access to all Pro features
                      </p>
                    </div>
                  )}
                </div>
              )}
            </CardFooter>
          </Card>
        </div>

        <div className="text-center mt-8">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Cancel anytime. No hidden fees. 
            {!isSubscribed && !trialExpired && (
              <span className="block mt-1">
                Your subscription will start after your 7-day free trial ends.
              </span>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
