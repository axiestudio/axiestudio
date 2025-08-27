import * as Form from "@radix-ui/react-form";
import { type FormEvent, useContext, useEffect, useState } from "react";
// import AxieStudioLogo from "@/assets/AxieStudioLogo.svg?react";
import InputComponent from "@/components/core/parameterRenderComponent/components/inputComponent";

import { useAddUser } from "@/controllers/API/queries/auth";
import { CustomLink } from "@/customization/components/custom-link";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { track } from "@/customization/utils/analytics";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Alert, AlertDescription } from "../../components/ui/alert";
import { Loader2, Mail, Shield, ArrowLeft } from "lucide-react";
import { api } from "../../controllers/API/api";
import { AuthContext } from "../../contexts/authContext";
import { SIGNUP_ERROR_ALERT } from "../../constants/alerts_constants";
import {
  CONTROL_INPUT_STATE,
  SIGN_UP_SUCCESS,
} from "../../constants/constants";
import useAlertStore from "../../stores/alertStore";
import type {
  inputHandlerEventType,
  signUpInputStateType,
  UserInputType,
} from "../../types/components";

interface SignupStep {
  step: 'signup' | 'verify-code' | 'success';
  email?: string;
  username?: string;
}

export default function SignUp(): JSX.Element {
  const [inputState, setInputState] =
    useState<signUpInputStateType>(CONTROL_INPUT_STATE);

  const [isDisabled, setDisableBtn] = useState<boolean>(true);

  // 🎯 NEW: Multi-step signup state
  const [currentStep, setCurrentStep] = useState<SignupStep>({ step: 'signup' });
  const [verificationCode, setVerificationCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [countdown, setCountdown] = useState(0);

  const { password, cnfPassword, username, email } = inputState;
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const navigate = useCustomNavigate();
  const { login } = useContext(AuthContext);

  const { mutate: mutateAddUser } = useAddUser();

  function handleInput({
    target: { name, value },
  }: inputHandlerEventType): void {
    setInputState((prev) => ({ ...prev, [name]: value }));
  }

  // Countdown timer for resend button
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  useEffect(() => {
    if (password !== cnfPassword) return setDisableBtn(true);
    if (password === "" || cnfPassword === "") return setDisableBtn(true);
    if (username === "") return setDisableBtn(true);
    setDisableBtn(false);
  }, [password, cnfPassword, username, handleInput]);

  function handleSignup(): void {
    const { username, password, email } = inputState;

    // Validate email is provided
    if (!email || !email.trim()) {
      setErrorData({
        title: SIGNUP_ERROR_ALERT,
        list: ["E-postadress krävs"],
      });
      return;
    }

    const newUser: UserInputType = {
      username: username.trim(),
      email: email.trim(),
      password: password.trim(),
    };

    mutateAddUser(newUser, {
      onSuccess: (user) => {
        track("User Signed Up", user);

        // � PRIMARY METHOD: Direct transition to code verification
        setCurrentStep({
          step: 'verify-code',
          email: newUser.email,
          username: newUser.username
        });
        setSuccess('✅ Konto skapat! Kontrollera din e-post för en 6-siffrig verifieringskod.');
        setCountdown(60); // 60 second cooldown for resend
      },
      onError: (error) => {
        const {
          response: {
            data: { detail },
          },
        } = error;
        setErrorData({
          title: SIGNUP_ERROR_ALERT,
          list: [detail],
        });
      },
    });
  }

  // 🎯 NEW: Code verification functions
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
          errorMessage += ` (${errorData.remaining_attempts} attempts remaining)`;
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

  // 🎯 Render functions for different steps
  const renderCodeStep = () => (
    <div className="h-screen w-full flex items-center justify-center bg-gradient-to-br from-background to-muted/30">
      <Card className="w-full max-w-md mx-auto">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <Shield className="w-6 h-6 text-green-600" />
          </div>
          <CardTitle className="text-2xl">Ange Verifieringskod</CardTitle>
          <CardDescription>
            Vi skickade en 6-siffrig kod till<br />
            <strong>{currentStep.email}</strong>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleVerifyCode} className="space-y-4">
            <div>
              <label htmlFor="code" className="block text-sm font-medium mb-2">
                6-Siffrig Kod
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
                'Verifiera & Aktivera Konto'
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
                {countdown > 0 ? `Skicka om om ${countdown}s` : 'Skicka Om Kod'}
              </Button>

              <br />

              <Button
                type="button"
                variant="ghost"
                onClick={() => setCurrentStep({ step: 'signup' })}
                className="text-sm"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Tillbaka till Registrering
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );

  const renderSuccessStep = () => (
    <div className="h-screen w-full flex items-center justify-center bg-gradient-to-br from-background to-muted/30">
      <Card className="w-full max-w-md mx-auto">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <Shield className="w-6 h-6 text-green-600" />
          </div>
          <CardTitle className="text-2xl text-green-600">Välkommen till AxieStudio!</CardTitle>
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
    </div>
  );

  // 🎯 Render based on current step
  if (currentStep.step === 'verify-code') {
    return renderCodeStep();
  }

  if (currentStep.step === 'success') {
    return renderSuccessStep();
  }

  // Default: render signup form
  return (
    <Form.Root
      onSubmit={(event: FormEvent<HTMLFormElement>) => {
        if (password === "") {
          event.preventDefault();
          return;
        }

        const _data = Object.fromEntries(new FormData(event.currentTarget));
        event.preventDefault();
      }}
      className="h-screen w-full"
    >
      <div className="flex h-full w-full flex-col items-center justify-center bg-muted">
        <div className="flex w-72 flex-col items-center justify-center gap-2">
          <img
            src="/logo192.png"
            alt="Axie Studio logo"
            className="mb-4 h-10 w-10 scale-[1.5] rounded"
            onError={(e) => {
              // Fallback to text logo if image fails to load
              e.currentTarget.style.display = 'none';
              e.currentTarget.nextElementSibling.style.display = 'flex';
            }}
          />
          <div
            className="mb-4 h-10 w-10 scale-[1.5] bg-primary text-primary-foreground rounded flex items-center justify-center font-bold text-lg"
            style={{ display: 'none' }}
          >
            AX
          </div>
          <span className="mb-6 text-2xl font-semibold text-primary">
            Registrera dig för Axie Studio
          </span>
          <div className="mb-3 w-full">
            <Form.Field name="username">
              <Form.Label className="data-[invalid]:label-invalid">
                Användarnamn <span className="font-medium text-destructive">*</span>
              </Form.Label>

              <Form.Control asChild>
                <Input
                  type="username"
                  onChange={({ target: { value } }) => {
                    handleInput({ target: { name: "username", value } });
                  }}
                  value={username}
                  className="w-full"
                  required
                  placeholder="Användarnamn"
                />
              </Form.Control>

              <Form.Message match="valueMissing" className="field-invalid">
                Vänligen ange ditt användarnamn
              </Form.Message>
            </Form.Field>
          </div>
          <div className="mb-3 w-full">
            <Form.Field name="email" serverInvalid={!email}>
              <Form.Label className="data-[invalid]:label-invalid">
                Email <span className="font-medium text-destructive">*</span>
              </Form.Label>

              <Form.Control asChild>
                <Input
                  type="email"
                  required
                  onChange={({ target: { value } }) => {
                    handleInput({ target: { name: "email", value } });
                  }}
                  value={email}
                  className="w-full"
                  placeholder="your@email.com"
                />
              </Form.Control>

              <Form.Message match="typeMismatch" className="field-invalid">
                Vänligen ange en giltig e-postadress
              </Form.Message>
              <Form.Message match="valueMissing" className="field-invalid">
                E-postadress krävs
              </Form.Message>
            </Form.Field>
          </div>
          <div className="mb-3 w-full">
            <Form.Field name="password" serverInvalid={password != cnfPassword}>
              <Form.Label className="data-[invalid]:label-invalid">
                Lösenord <span className="font-medium text-destructive">*</span>
              </Form.Label>
              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "password", value } });
                }}
                value={password}
                isForm
                password={true}
                required
                placeholder="Lösenord"
                className="w-full"
              />

              <Form.Message className="field-invalid" match="valueMissing">
                Vänligen ange ett lösenord
              </Form.Message>

              {password != cnfPassword && (
                <Form.Message className="field-invalid">
                  Lösenorden stämmer inte överens
                </Form.Message>
              )}


            </Form.Field>
          </div>
          <div className="w-full">
            <Form.Field
              name="confirmpassword"
              serverInvalid={password != cnfPassword}
            >
              <Form.Label className="data-[invalid]:label-invalid">
                Bekräfta ditt lösenord{" "}
                <span className="font-medium text-destructive">*</span>
              </Form.Label>

              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "cnfPassword", value } });
                }}
                value={cnfPassword}
                isForm
                password={true}
                required
                placeholder="Bekräfta ditt lösenord"
                className="w-full"
              />

              <Form.Message className="field-invalid" match="valueMissing">
                Vänligen bekräfta ditt lösenord
              </Form.Message>
            </Form.Field>
          </div>
          <div className="w-full">
            <Form.Submit asChild>
              <Button
                disabled={isDisabled}
                type="submit"
                className="mr-3 mt-6 w-full"
                onClick={() => {
                  handleSignup();
                }}
              >
                Registrera dig
              </Button>
            </Form.Submit>
          </div>
          <div className="w-full space-y-3">
            <CustomLink to="/login">
              <Button className="w-full" variant="outline">
                Har du redan ett konto?&nbsp;<b>Logga in</b>
              </Button>
            </CustomLink>

            {/* 🎯 TERTIARY METHOD: Account not activated backup */}
            <div className="text-center">
              <CustomLink to="/verify-email" className="text-sm text-muted-foreground hover:text-primary">
                Konto inte aktiverat? <span className="underline">Klicka här</span>
              </CustomLink>
            </div>
          </div>
        </div>
      </div>
    </Form.Root>
  );
}
