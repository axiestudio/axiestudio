import { useEffect, useState, useContext } from "react";
import { useSearchParams } from "react-router-dom";
import { CustomLink } from "@/customization/components/custom-link";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { Button } from "../../components/ui/button";
import useAlertStore from "../../stores/alertStore";
import { AuthContext } from "../../contexts/authContext";
import { api } from "../../controllers/API/api";

export default function ResetPasswordPage(): JSX.Element {
  const [searchParams] = useSearchParams();
  const [isLoading, setIsLoading] = useState(true);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useCustomNavigate();
  const { login } = useContext(AuthContext);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  const token = searchParams.get("token");

  useEffect(() => {
    if (!token) {
      setError("Ogiltig återställningslänk. Vänligen begär en ny lösenordsåterställning.");
      setIsLoading(false);
      return;
    }

    handlePasswordReset();
  }, [token]);

  const handlePasswordReset = async () => {
    try {
      const response = await api.get(`/api/v1/email/reset-password?token=${token}`);
      
      if (response.data.access_token) {
        // Log the user in automatically
        login(response.data.access_token, "password_reset", response.data.refresh_token);
        
        setIsSuccess(true);
        setSuccessData({
          title: "Lösenordsåterställning lyckades! Du är nu inloggad. Gå till Inställningar för att ändra ditt lösenord.",
        });
        
        // Redirect to settings after a short delay
        setTimeout(() => {
          navigate("/settings");
        }, 3000);
      }
      
    } catch (error: any) {
      const errorMessage = error?.response?.data?.detail || "Ogiltig eller utgången återställningslänk.";
      setError(errorMessage);
      setErrorData({
        title: "Lösenordsåterställning Misslyckades",
        list: [errorMessage],
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="h-screen w-full">
        <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-background to-muted/30">
          <div className="flex w-96 flex-col items-center justify-center gap-6 rounded-2xl bg-card/80 backdrop-blur-sm border border-border/50 p-8 shadow-2xl">
            <div className="flex flex-col items-center gap-4">
              <img
                src="/logo192.png"
                alt="Axie Studio logo"
                className="h-12 w-12 rounded-xl object-contain"
                onError={(e) => {
                  // Fallback to text logo if image fails to load
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.nextElementSibling.style.display = 'flex';
                }}
              />
              <div className="h-12 w-12 bg-primary text-primary-foreground rounded-xl items-center justify-center font-bold text-lg hidden">
                AS
              </div>
              <div className="text-center">
                <h1 className="text-2xl font-light text-foreground tracking-tight">
                  Bearbetar Återställningslänk...
                </h1>
                <p className="text-sm text-muted-foreground mt-1">
                  Vänligen vänta medan vi verifierar din återställningstoken
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="h-screen w-full">
        <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-background to-muted/30">
          <div className="flex w-96 flex-col items-center justify-center gap-6 rounded-2xl bg-card/80 backdrop-blur-sm border border-border/50 p-8 shadow-2xl">
            <div className="flex flex-col items-center gap-4 text-center">
              <img
                src="/logo192.png"
                alt="Axie Studio logo"
                className="h-12 w-12 rounded-xl object-contain"
                onError={(e) => {
                  // Fallback to text logo if image fails to load
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.nextElementSibling.style.display = 'flex';
                }}
              />
              <div className="h-12 w-12 bg-primary text-primary-foreground rounded-xl items-center justify-center font-bold text-lg hidden">
                AS
              </div>
              <div>
                <h1 className="text-2xl font-light text-foreground tracking-tight">
                  Lösenordsåterställning Lyckades!
                </h1>
                <p className="text-sm text-muted-foreground mt-2">
                  Du är nu inloggad på ditt konto
                </p>
              </div>
            </div>
            
            <div className="w-full space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-sm text-green-800">
                  <strong>Du är inloggad!</strong><br/>
                  <strong>Ange ett nytt lösenord</strong> för att säkra ditt konto<br/>
                  <strong>Välj ett starkt lösenord</strong> för att hålla ditt konto säkert
                </p>
              </div>

              <Button
                onClick={() => navigate("/change-password?from_reset=true")}
                className="w-full h-11 bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
              >
                Ange Nytt Lösenord
              </Button>
              
              <div className="text-center">
                <p className="text-sm text-muted-foreground">
                  <CustomLink to="/" className="text-primary hover:underline font-medium">
                    Fortsätt till Instrumentpanel
                  </CustomLink>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen w-full">
        <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-background to-muted/30">
          <div className="flex w-96 flex-col items-center justify-center gap-6 rounded-2xl bg-card/80 backdrop-blur-sm border border-border/50 p-8 shadow-2xl">
            <div className="flex flex-col items-center gap-4 text-center">
              <img
                src="/logo192.png"
                alt="Axie Studio logo"
                className="h-12 w-12 rounded-xl object-contain"
                onError={(e) => {
                  // Fallback to text logo if image fails to load
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.nextElementSibling.style.display = 'flex';
                }}
              />
              <div className="h-12 w-12 bg-primary text-primary-foreground rounded-xl items-center justify-center font-bold text-lg hidden">
                AS
              </div>
              <div>
                <h1 className="text-2xl font-light text-foreground tracking-tight">
                  Återställningslänk Ogiltig
                </h1>
                <p className="text-sm text-muted-foreground mt-2">
                  {error}
                </p>
              </div>
            </div>
            
            <div className="w-full space-y-4">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">
                  🚨 <strong>Denna återställningslänk är ogiltig eller har gått ut</strong><br/>
                  🔗 <strong>Begär en ny återställningslänk</strong> från inloggningssidan<br/>
                  ⏰ <strong>Återställningslänkar går ut efter 24 timmar</strong>
                </p>
              </div>
              
              <Button 
                onClick={() => navigate("/forgot-password")}
                className="w-full h-11 bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
              >
                Begär Ny Återställningslänk
              </Button>
              
              <div className="text-center">
                <p className="text-sm text-muted-foreground">
                  <CustomLink to="/login" className="text-primary hover:underline font-medium">
                    Tillbaka till inloggning
                  </CustomLink>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
