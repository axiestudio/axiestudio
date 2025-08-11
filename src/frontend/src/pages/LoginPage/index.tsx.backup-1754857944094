import * as Form from "@radix-ui/react-form";
import { useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { useLoginUser } from "@/controllers/API/queries/auth";
import { CustomLink } from "@/customization/components/custom-link";
import InputComponent from "../../components/core/parameterRenderComponent/components/inputComponent";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { LanguageSwitcher } from "../../components/ui/language-switcher";
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
  const { t } = useTranslation();
  const [inputState, setInputState] =
    useState<loginInputStateType>(CONTROL_LOGIN_STATE);

  const { password, username } = inputState;
  const { login } = useContext(AuthContext);
  const setErrorData = useAlertStore((state) => state.setErrorData);

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
        login(data.access_token, "login", data.refresh_token);
      },
      onError: (error) => {
        setErrorData({
          title: t('errors.signinError'),
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
        <div className="flex w-96 flex-col items-center justify-center gap-6 rounded-2xl bg-card/80 backdrop-blur-sm border border-border/50 p-8 shadow-2xl relative">
          {/* Language Switcher */}
          <div className="absolute top-4 right-4">
            <LanguageSwitcher variant="compact" />
          </div>
          <div className="flex flex-col items-center gap-4">
            <img
              src="/logo.jpg"
              alt="Axie Studio logo"
              className="h-12 w-12 rounded-xl object-contain"
              onError={(e) => {
                e.currentTarget.src = "/logo.svg";
              }}
              style={{ maxWidth: '48px', maxHeight: '48px' }}
            />
            <div className="text-center">
              <h1 className="text-2xl font-light text-foreground tracking-tight">
                {t('auth.welcome')}
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                {t('auth.signInSubtitle')}
              </p>
            </div>
          </div>
          <div className="w-full space-y-5">
            <Form.Field name="username">
              <Form.Label className="text-sm font-medium text-foreground data-[invalid]:text-destructive">
                {t('auth.username')}
              </Form.Label>
              <Form.Control asChild>
                <Input
                  type="username"
                  onChange={({ target: { value } }) => {
  const { t } = useTranslation();
                    handleInput({ target: { name: "username", value } });
                  }}
                  value={username}
                  className="w-full h-11 mt-2 border-border/60 focus:border-primary/60 focus:ring-1 focus:ring-primary/20"
                  required
                  placeholder={t('auth.enterUsername')}
                />
              </Form.Control>
              <Form.Message match="valueMissing" className="text-xs text-destructive mt-1">
                {t('auth.pleaseEnterUsername')}
              </Form.Message>
            </Form.Field>

            <Form.Field name="password">
              <Form.Label className="text-sm font-medium text-foreground data-[invalid]:text-destructive">
                {t('auth.password')}
              </Form.Label>
              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "password", value } });
                }}
                value={password}
                isForm
                password={true}
                required
                placeholder={t('auth.enterPassword')}
                className="w-full h-11 mt-2 border-border/60 focus:border-primary/60 focus:ring-1 focus:ring-primary/20"
              />
              <Form.Message className="text-xs text-destructive mt-1" match="valueMissing">
                {t('auth.pleaseEnterPassword')}
              </Form.Message>
            </Form.Field>

            <Form.Submit asChild>
              <Button className="w-full h-11 mt-8 bg-primary hover:bg-primary/90 text-primary-foreground font-medium" type="submit">
                {t('auth.signIn')}
              </Button>
            </Form.Submit>
          </div>

        </div>
      </div>
    </Form.Root>
  );
}
