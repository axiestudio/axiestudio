import { useContext, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Alert, AlertDescription } from "../../components/ui/alert";
import { Loader2, Mail, Shield, ArrowLeft } from "lucide-react";
import { useCustomNavigate } from "../../customization/hooks/use-custom-navigate";
import { CustomLink } from "../../customization/components/custom-link";
import { AuthContext } from "../../contexts/authContext";
import { api } from "../../controllers/API/api";

interface VerificationStep {
  step: 'email' | 'code' | 'success' | 'token-verify';
  email?: string;
}

export default function EmailVerificationPage(): JSX.Element {
  const [searchParams] = useSearchParams();
  const navigate = useCustomNavigate();
  const { login } = useContext(AuthContext);
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");
  const [isResending, setIsResending] = useState(false);

  // 🎯 NEW: 6-digit code verification state
  const [currentStep, setCurrentStep] = useState<VerificationStep>({ step: 'email' });
  const [email, setEmail] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [countdown, setCountdown] = useState(0);

  const token = searchParams.get("token");

  // Countdown timer for resend button
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  useEffect(() => {
    if (token) {
      // Legacy token-based verification
      setCurrentStep({ step: 'token-verify' });
      verifyEmail(token);
    } else {
      // New 6-digit code verification flow
      setCurrentStep({ step: 'email' });
      setStatus("loading"); // Reset status for code flow
    }
  }, [token]);

  const verifyEmail = async (verificationToken: string) => {
    try {
      const response = await api.get(`/api/v1/email/verify?token=${verificationToken}`);

      if (response.data.verified) {
        setStatus("success");

        // Check if auto-login tokens are provided
        if (response.data.access_token && response.data.auto_login) {
          // Log the user in automatically
          login(response.data.access_token, "email_verification", response.data.refresh_token);
          setMessage("E-post verifierad framgångsrikt! Du är nu inloggad. Omdirigerar till instrumentpanel...");

          // Redirect to dashboard after a short delay
          setTimeout(() => {
            navigate("/");
          }, 2000);
        } else {
          setMessage("E-post verifierad framgångsrikt! Du kan nu logga in på ditt konto.");
        }
      } else {
        setStatus("error");
        setMessage("E-postverifiering misslyckades. Vänligen försök igen.");
      }
    } catch (error: any) {
      setStatus("error");
      const errorMessage = error?.response?.data?.detail || "E-postverifiering misslyckades. Länken kan vara utgången eller ogiltig.";
      setMessage(errorMessage);
    }
  };

  const resendVerificationEmail = async () => {
    const email = prompt("Vänligen ange din e-postadress för att skicka verifiering igen:");
    
    if (!email) return;

    setIsResending(true);
    
    try {
      await api.post(`/api/v1/email/resend-verification`, { email });
      setMessage("Verifieringsmail skickat! Vänligen kontrollera din inkorg.");
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || "Misslyckades att skicka verifieringsmail igen.";
      setMessage(errorMessage);
    } finally {
      setIsResending(false);
    }
  };

  const goToLogin = () => {
    navigate("/login");
  };

  // 🎯 NEW: 6-digit code verification functions
  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await api.post('/api/v1/email/resend-code', { email });

      if (response.data) {
        setCurrentStep({ step: 'code', email });
        setSuccess('✅ Verifieringskod skickad! Kontrollera din e-post.');
        setCountdown(60); // 60 second cooldown
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Misslyckades att skicka verifieringskod';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyCode = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await api.post('/api/v1/email/verify-code', {
        email: currentStep.email,
        code: verificationCode
      });

      if (response.data) {
        // Auto-login if tokens provided
        if (response.data.access_token) {
          login(response.data.access_token, "email_verification", response.data.refresh_token);
        }

        setCurrentStep({ step: 'success' });
        setSuccess('🎉 Konto aktiverat framgångsrikt!');

        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
          navigate('/');
        }, 2000);
      }
    } catch (err: any) {
      const errorData = err.response?.data?.detail;
      let errorMessage = 'Ogiltig verifieringskod';

      if (typeof errorData === 'object') {
        errorMessage = errorData.message || errorMessage;
        if (errorData.remaining_attempts !== undefined) {
          errorMessage += ` (${errorData.remaining_attempts} försök kvar)`;
        }
      } else if (typeof errorData === 'string') {
        errorMessage = errorData;
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendCode = async () => {
    if (countdown > 0) return;

    setIsLoading(true);
    setError('');

    try {
      await api.post('/api/v1/email/resend-code', { email: currentStep.email });
      setSuccess('✅ Ny verifieringskod skickad!');
      setCountdown(60);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Misslyckades att skicka om kod');
    } finally {
      setIsLoading(false);
    }
  };

  // 🎯 NEW: Render functions for 6-digit code flow
  const renderEmailStep = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <img
          src="/logo192.png"
          alt="Axie Studio logo"
          className="mx-auto mb-4 w-12 h-12 rounded-full object-contain"
          onError={(e) => {
            // Fallback to text logo if image fails to load
            e.currentTarget.style.display = 'none';
            e.currentTarget.nextElementSibling.style.display = 'flex';
          }}
        />
        <div className="mx-auto mb-4 w-12 h-12 bg-primary text-primary-foreground rounded-full items-center justify-center font-bold text-sm hidden">
          AS
        </div>
        <CardTitle className="text-2xl">Konto inte aktiverat?</CardTitle>
        <CardDescription>
          Ange din e-postadress för att få en verifieringskod
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSendCode} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-2">
              E-postadress
            </label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Ange din e-postadress"
              required
              disabled={isLoading}
            />
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert>
              <AlertDescription>{success}</AlertDescription>
            </Alert>
          )}

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Skickar kod...
              </>
            ) : (
              'Skicka verifieringskod'
            )}
          </Button>

          <div className="text-center">
            <Button
              type="button"
              variant="ghost"
              onClick={() => navigate('/login')}
              className="text-sm"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Tillbaka till inloggning
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );

  const renderCodeStep = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <img
          src="/logo192.png"
          alt="Axie Studio logo"
          className="mx-auto mb-4 w-12 h-12 rounded-full object-contain"
          onError={(e) => {
            // Fallback to text logo if image fails to load
            e.currentTarget.style.display = 'none';
            e.currentTarget.nextElementSibling.style.display = 'flex';
          }}
        />
        <div className="mx-auto mb-4 w-12 h-12 bg-primary text-primary-foreground rounded-full items-center justify-center font-bold text-sm hidden">
          AS
        </div>
        <CardTitle className="text-2xl">Ange verifieringskod</CardTitle>
        <CardDescription>
          Vi skickade en 6-siffrig kod till<br />
          <strong>{currentStep.email}</strong>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleVerifyCode} className="space-y-4">
          <div>
            <label htmlFor="code" className="block text-sm font-medium mb-2">
              6-siffrig kod
            </label>
            <Input
              id="code"
              type="text"
              value={verificationCode}
              onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              placeholder="123456"
              required
              disabled={isLoading}
              className="text-center text-2xl tracking-widest"
              maxLength={6}
            />
            <p className="text-xs text-gray-500 mt-1">
              ⏰ Koden går ut om 10 minuter
            </p>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert>
              <AlertDescription>{success}</AlertDescription>
            </Alert>
          )}

          <Button type="submit" className="w-full" disabled={isLoading || verificationCode.length !== 6}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Verifierar...
              </>
            ) : (
              'Verifiera & aktivera konto'
            )}
          </Button>

          <div className="text-center space-y-2">
            <Button
              type="button"
              variant="ghost"
              onClick={handleResendCode}
              disabled={countdown > 0 || isLoading}
              className="text-sm"
            >
              {countdown > 0 ? `Skicka igen om ${countdown}s` : 'Skicka kod igen'}
            </Button>

            <br />

            <Button
              type="button"
              variant="ghost"
              onClick={() => setCurrentStep({ step: 'email' })}
              className="text-sm"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Ändra e-post
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );

  const renderSuccessStep = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <img
          src="/logo192.png"
          alt="Axie Studio logo"
          className="mx-auto mb-4 w-12 h-12 rounded-full object-contain"
          onError={(e) => {
            // Fallback to text logo if image fails to load
            e.currentTarget.style.display = 'none';
            e.currentTarget.nextElementSibling.style.display = 'flex';
          }}
        />
        <div className="mx-auto mb-4 w-12 h-12 bg-primary text-primary-foreground rounded-full items-center justify-center font-bold text-sm hidden">
          AS
        </div>
        <CardTitle className="text-2xl text-green-600">Konto aktiverat!</CardTitle>
        <CardDescription>
          Ditt konto har aktiverats framgångsrikt.<br />
          Omdirigerar till instrumentpanel...
        </CardDescription>
      </CardHeader>
      <CardContent className="text-center">
        <div className="animate-spin mx-auto w-8 h-8 border-4 border-green-200 border-t-green-600 rounded-full mb-4"></div>
        <p className="text-sm text-gray-600">
          Du kan nu komma åt alla funktioner i AxieStudio!
        </p>
      </CardContent>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <img
            src="/logo192.png"
            alt="Axie Studio logo"
            className="mx-auto w-16 h-16 rounded-full object-contain mb-4"
            onError={(e) => {
              // Fallback to text logo if image fails to load
              e.currentTarget.style.display = 'none';
              e.currentTarget.nextElementSibling.style.display = 'flex';
            }}
          />
          <div className="mx-auto w-16 h-16 bg-primary text-primary-foreground rounded-full items-center justify-center mb-4 font-bold text-xl hidden">
            AS
          </div>
          <h1 className="text-2xl font-bold text-gray-900">AxieStudio</h1>
          <p className="text-gray-600">E-postverifiering</p>
        </div>

        {/* Render based on current step */}
        {currentStep.step === 'email' && renderEmailStep()}
        {currentStep.step === 'code' && renderCodeStep()}
        {currentStep.step === 'success' && renderSuccessStep()}

        {/* Legacy token-based verification */}
        {currentStep.step === 'token-verify' && (
          <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
            <div className="flex flex-col space-y-2 text-center">
              <h1 className="text-2xl font-semibold tracking-tight">
                E-postverifiering
              </h1>
          
          {status === "loading" && (
            <div className="flex flex-col items-center space-y-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              <p className="text-sm text-muted-foreground">
                Verifierar din e-postadress...
              </p>
            </div>
          )}

          {status === "success" && (
            <div className="flex flex-col items-center space-y-4">
              <div className="rounded-full bg-green-100 p-3">
                <svg
                  className="h-6 w-6 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <p className="text-sm text-muted-foreground">{message}</p>
              <Button onClick={goToLogin} className="w-full">
                Gå till inloggning
              </Button>
            </div>
          )}

          {status === "error" && (
            <div className="flex flex-col items-center space-y-4">
              <div className="rounded-full bg-red-100 p-3">
                <svg
                  className="h-6 w-6 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </div>
              <p className="text-sm text-muted-foreground">{message}</p>
              
              <div className="flex flex-col space-y-2 w-full">
                <Button 
                  onClick={resendVerificationEmail} 
                  variant="outline" 
                  className="w-full"
                  disabled={isResending}
                >
                  {isResending ? "Skickar..." : "Skicka verifieringsmail igen"}
                </Button>
                
                <CustomLink to="/login" className="text-center">
                  <Button variant="ghost" className="w-full">
                    Tillbaka till inloggning
                  </Button>
                </CustomLink>
              </div>
            </div>
          )}
            </div>
          </div>
        )}

        {/* Help text */}
        <div className="text-center mt-6 text-sm text-gray-500">
          <p>Behöver du hjälp? Kontakta vårt supportteam</p>
        </div>
      </div>
    </div>
  );
}
