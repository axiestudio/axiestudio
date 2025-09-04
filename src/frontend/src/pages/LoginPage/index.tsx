import * as Form from "@radix-ui/react-form";
import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLoginUser } from "@/controllers/API/queries/auth";
import { CustomLink } from "@/customization/components/custom-link";
import InputComponent from "../../components/core/parameterRenderComponent/components/inputComponent";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { SIGNIN_ERROR_ALERT } from "../../constants/alerts_constants";
import { CONTROL_LOGIN_STATE } from "../../constants/constants";
import { AuthContext } from "../../contexts/authContext";
import useAlertStore from "../../stores/alertStore";
import type { LoginType } from "../../types/api";
import type {
  inputHandlerEventType,
  loginInputStateType,
} from "../../types/components";

export default function LoginPage(): JSX.Element {
  const [inputState, setInputState] =
    useState<loginInputStateType>(CONTROL_LOGIN_STATE);

  const { password, username } = inputState;
  const { login } = useContext(AuthContext);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const navigate = useNavigate();

  function handleInput({
    target: { name, value },
  }: inputHandlerEventType): void {
    setInputState((prev) => ({ ...prev, [name]: value }));
  }

  const { mutate } = useLoginUser();

  function signIn() {
    const user: LoginType = {
      username: username.trim(),
      password: password.trim(),
    };

    mutate(user, {
      onSuccess: (data) => {
        // Check if password change is required (temporary password scenario)
        if (data.password_change_required) {
          // Log the user in first
          login(data.access_token, "login", data.refresh_token);
          // Then redirect to change password page with a flag
          navigate("/change-password?from_reset=true");
        } else {
          // Normal login flow
          login(data.access_token, "login", data.refresh_token);
        }
      },
      onError: (error) => {
        setErrorData({
          title: SIGNIN_ERROR_ALERT,
          list: [error["response"]["data"]["detail"]],
        });
      },
    });
  }

  return (
    <Form.Root
      onSubmit={(event) => {
        if (password === "") {
          event.preventDefault();
          return;
        }
        signIn();
        const _data = Object.fromEntries(new FormData(event.currentTarget));
        event.preventDefault();
      }}
      className="h-screen w-full"
    >
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
              style={{ maxWidth: '48px', maxHeight: '48px' }}
            />
            <div
              className="h-12 w-12 bg-primary text-primary-foreground rounded-xl flex items-center justify-center font-bold text-lg"
              style={{ display: 'none' }}
            >
              AX
            </div>
            <div className="text-center">
              <h1 className="text-2xl font-light text-foreground tracking-tight">
                Välkommen till Axie Studio
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Logga in för att fortsätta till din arbetsyta
              </p>
            </div>
          </div>
          <div className="w-full space-y-5">
            <Form.Field name="username">
              <Form.Label className="text-sm font-medium text-foreground data-[invalid]:text-destructive">
                Användarnamn
              </Form.Label>
              <Form.Control asChild>
                <Input
                  type="username"
                  onChange={({ target: { value } }) => {
                    handleInput({ target: { name: "username", value } });
                  }}
                  value={username}
                  className="w-full h-11 mt-2 border-border/60 focus:border-primary/60 focus:ring-1 focus:ring-primary/20"
                  required
                  placeholder="Ange ditt användarnamn"
                />
              </Form.Control>
              <Form.Message match="valueMissing" className="text-xs text-destructive mt-1">
                Vänligen ange ditt användarnamn
              </Form.Message>
            </Form.Field>

            <Form.Field name="password">
              <Form.Label className="text-sm font-medium text-foreground data-[invalid]:text-destructive">
                Lösenord
              </Form.Label>
              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "password", value } });
                }}
                value={password}
                isForm
                password={true}
                required
                placeholder="Ange ditt lösenord"
                className="w-full h-11 mt-2 border-border/60 focus:border-primary/60 focus:ring-1 focus:ring-primary/20"
              />
              <Form.Message className="text-xs text-destructive mt-1" match="valueMissing">
                Vänligen ange ditt lösenord
              </Form.Message>
            </Form.Field>

            <Form.Submit asChild>
              <Button className="w-full h-11 mt-8 bg-primary hover:bg-primary/90 text-primary-foreground font-medium" type="submit">
                Logga in
              </Button>
            </Form.Submit>

            <div className="text-center mt-4 space-y-2">
              <p className="text-sm text-muted-foreground">
                <CustomLink to="/forgot-password" className="text-primary hover:underline font-medium">
                  Glömt ditt lösenord?
                </CustomLink>
              </p>
              <p className="text-sm text-muted-foreground">
                <CustomLink to="/verify-email" className="text-primary hover:underline font-medium">
                  Konto inte aktiverat?
                </CustomLink>
              </p>
              <p className="text-sm text-muted-foreground">
                Har du inget konto?{" "}
                <CustomLink to="/signup" className="text-primary hover:underline font-medium">
                  Registrera dig
                </CustomLink>
              </p>
            </div>
          </div>

        </div>
      </div>
    </Form.Root>
  );
}
