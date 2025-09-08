import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, Crown, ArrowRight, Loader2 } from "lucide-react";
import { api } from "@/controllers/API";
import { getURL } from "@/utils";

export default function SubscriptionSuccessPage(): JSX.Element {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [verificationStatus, setVerificationStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [verificationMessage, setVerificationMessage] = useState('Verifierar din prenumeration...');

  useEffect(() => {
    const sessionId = searchParams.get('session_id');

    // Verify subscription with backend
    const verifySubscription = async () => {
      if (sessionId) {
        try {
          const response = await api.get(`${getURL()}/api/v1/subscriptions/success?session_id=${sessionId}`);
          if (response.status === 200) {
            setVerificationStatus('success');
            setVerificationMessage('Prenumeration bekräftad! Välkommen till AxieStudio Pro!');
          } else {
            setVerificationStatus('error');
            setVerificationMessage('Kunde inte verifiera prenumeration. Kontakta support om problemet kvarstår.');
          }
        } catch (error) {
          console.error('Subscription verification error:', error);
          setVerificationStatus('error');
          setVerificationMessage('Verifieringsfel. Din prenumeration kan fortfarande vara aktiv.');
        }
      } else {
        setVerificationStatus('success');
        setVerificationMessage('Prenumeration aktiverad!');
      }
    };

    verifySubscription();

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
            {verificationStatus === 'loading' ? (
              <Loader2 className="h-8 w-8 text-green-600 dark:text-green-400 animate-spin" />
            ) : (
              <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
            )}
          </div>
          <CardTitle className="text-2xl text-green-900 dark:text-green-100">
            {verificationStatus === 'loading' ? 'Verifierar...' : 'Välkommen till Pro!'}
          </CardTitle>
          <CardDescription className="text-green-700 dark:text-green-300">
            {verificationMessage}
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Crown className="h-5 w-5 text-green-600 dark:text-green-400" />
              <span className="font-medium text-green-900 dark:text-green-100">
                Pro-prenumeration Aktiv
              </span>
            </div>
            <p className="text-sm text-green-700 dark:text-green-300">
              Du har nu åtkomst till alla Pro-funktioner och obegränsad användning.
            </p>
          </div>

          <div className="space-y-3 text-left">
            <h3 className="font-medium text-center mb-3">Vad som ingår:</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Obegränsad AI-arbetsflödesautomation</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Prioriterad kundsupport</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Avancerade integrationer</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm">Teamsamarbetsfunktioner</span>
              </div>
            </div>
          </div>

          <Button onClick={handleContinue} className="w-full">
            Fortsätt till Axie Studio
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>

          <p className="text-xs text-muted-foreground">
            Du kommer automatiskt att omdirigeras om några sekunder...
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
