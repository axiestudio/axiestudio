import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { useCustomNavigate } from "../../customization/hooks/use-custom-navigate";
import { CustomLink } from "../../customization/components/custom-link";
import { api } from "../../controllers/API/api";

export default function EmailVerificationPage(): JSX.Element {
  const [searchParams] = useSearchParams();
  const navigate = useCustomNavigate();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");
  const [isResending, setIsResending] = useState(false);

  const token = searchParams.get("token");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Invalid verification link. Please check your email for the correct link.");
      return;
    }

    verifyEmail(token);
  }, [token]);

  const verifyEmail = async (verificationToken: string) => {
    try {
      const response = await api.get(`/api/v1/email/verify?token=${verificationToken}`);
      
      if (response.data.verified) {
        setStatus("success");
        setMessage("Email verified successfully! You can now log in to your account.");
      } else {
        setStatus("error");
        setMessage("Email verification failed. Please try again.");
      }
    } catch (error: any) {
      setStatus("error");
      const errorMessage = error?.response?.data?.detail || "Email verification failed. The link may be expired or invalid.";
      setMessage(errorMessage);
    }
  };

  const resendVerificationEmail = async () => {
    const email = prompt("Please enter your email address to resend verification:");
    
    if (!email) return;

    setIsResending(true);
    
    try {
      await api.post(`/api/v1/email/resend-verification`, { email });
      setMessage("Verification email sent! Please check your inbox.");
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || "Failed to resend verification email.";
      setMessage(errorMessage);
    } finally {
      setIsResending(false);
    }
  };

  const goToLogin = () => {
    navigate("/login");
  };

  return (
    <div className="flex h-screen w-full flex-col items-center justify-center bg-muted">
      <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
        <div className="flex flex-col space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">
            Email Verification
          </h1>
          
          {status === "loading" && (
            <div className="flex flex-col items-center space-y-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              <p className="text-sm text-muted-foreground">
                Verifying your email address...
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
                Go to Login
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
                  {isResending ? "Sending..." : "Resend Verification Email"}
                </Button>
                
                <CustomLink to="/login" className="text-center">
                  <Button variant="ghost" className="w-full">
                    Back to Login
                  </Button>
                </CustomLink>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
