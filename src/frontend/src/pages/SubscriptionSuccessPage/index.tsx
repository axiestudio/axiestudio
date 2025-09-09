import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, Crown, ArrowRight, Loader2 } from "lucide-react";
import { api } from "@/controllers/API/api";
import { getURL } from "@/controllers/API/helpers/constants";
import { useSubscriptionStore } from "@/stores/subscriptionStore";
import { useRealtimeSubscriptionContext, triggerSubscriptionRefresh } from "@/components/providers/RealtimeSubscriptionProvider";

export default function SubscriptionSuccessPage(): JSX.Element {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [isVerifying, setIsVerifying] = useState(true);
  const [verificationStatus, setVerificationStatus] = useState<'success' | 'error' | 'pending'>('pending');
  const { refreshStatus, startFastPolling } = useSubscriptionStore();
  const { forceRefresh } = useRealtimeSubscriptionContext();

  useEffect(() => {
    // Get session_id from URL parameters
    const sessionId = searchParams.get('session_id');

    if (sessionId) {
      // Call backend to verify and activate subscription
      const verifySubscription = async () => {
        try {
          await api.get(`${getURL("SUBSCRIPTIONS")}/success?session_id=${sessionId}`);
          setVerificationStatus('success');
          console.log('✅ Subscription verified and activated');

          // CRITICAL FIX: Multi-layer subscription refresh for maximum reliability
          try {
            console.log('🚀 Starting comprehensive subscription verification...');

            // 1. Immediate store refresh
            await refreshStatus();
            console.log('✅ Store subscription status refreshed');

            // 2. Real-time provider refresh
            await forceRefresh('payment success verification');
            console.log('✅ Real-time subscription status refreshed');

            // 3. Trigger cross-tab synchronization
            triggerSubscriptionRefresh('payment success');
            console.log('✅ Cross-tab subscription sync triggered');

            // 4. Start fast polling for webhook updates
            startFastPolling();
            console.log('🚀 Fast polling started for webhook updates');

          } catch (refreshError) {
            console.warn('⚠️ Failed to refresh subscription status:', refreshError);
          }
        } catch (error) {
          console.error('❌ Subscription verification failed:', error);
          setVerificationStatus('error');
        } finally {
          setIsVerifying(false);
        }
      };

      verifySubscription();
    } else {
      // No session ID, assume success from webhook
      setIsVerifying(false);
      setVerificationStatus('success');

      // CRITICAL FIX: Also refresh status when no session ID (webhook success)
      try {
        refreshStatus();
        console.log('✅ Subscription status refreshed for webhook success');

        // Start fast polling to catch any delayed webhook updates
        startFastPolling();
        console.log('🚀 Started fast polling for webhook success');
      } catch (refreshError) {
        console.warn('⚠️ Failed to refresh subscription status:', refreshError);
      }
    }

    // Auto-redirect after 10 seconds
    const timer = setTimeout(() => {
      navigate("/");
    }, 10000);

    return () => clearTimeout(timer);
  }, [navigate, searchParams]);

  const handleContinue = () => {
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <Card className="max-w-md w-full text-center">
        <CardHeader className="pb-4">
          <div className="mx-auto mb-4 w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
            {isVerifying ? (
              <Loader2 className="h-8 w-8 text-blue-600 dark:text-blue-400 animate-spin" />
            ) : verificationStatus === 'success' ? (
              <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
            ) : (
              <CheckCircle className="h-8 w-8 text-yellow-600 dark:text-yellow-400" />
            )}
          </div>
          <CardTitle className="text-2xl text-green-900 dark:text-green-100">
            {isVerifying ? "Activating..." : "Welcome to Pro!"}
          </CardTitle>
          <CardDescription className="text-green-700 dark:text-green-300">
            {isVerifying
              ? "We're activating your subscription..."
              : verificationStatus === 'success'
              ? "Your subscription has been successfully activated"
              : "Your subscription is being processed"
            }
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Crown className="h-5 w-5 text-green-600 dark:text-green-400" />
              <span className="font-medium text-green-900 dark:text-green-100">
                Pro Subscription Active
              </span>
            </div>
            <p className="text-sm text-green-700 dark:text-green-300">
              You now have access to all Pro features and unlimited usage.
            </p>
          </div>

          <div className="space-y-3 text-left">
            <h3 className="font-medium text-center mb-3">What's included:</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Unlimited AI workflow automation</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Priority customer support</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Advanced integrations</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Team collaboration features</span>
              </div>
            </div>
          </div>

          <Button onClick={handleContinue} className="w-full">
            Continue to Axie Studio
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>

          <p className="text-xs text-muted-foreground">
            You'll be automatically redirected in a few seconds...
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
