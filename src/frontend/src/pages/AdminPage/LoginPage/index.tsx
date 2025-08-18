import { useContext, useState } from "react";
import { useLoginUser } from "@/controllers/API/queries/auth";
import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import { SIGNIN_ERROR_ALERT } from "../../../constants/alerts_constants";
import { CONTROL_LOGIN_STATE } from "../../../constants/constants";
import { AuthContext } from "../../../contexts/authContext";
import useAlertStore from "../../../stores/alertStore";
import type { LoginType } from "../../../types/api";
import type {
  inputHandlerEventType,
  loginInputStateType,
} from "../../../types/components";

export default function LoginAdminPage() {
  const [inputState, setInputState] =
    useState<loginInputStateType>(CONTROL_LOGIN_STATE);
  const { login } = useContext(AuthContext);

  const { password, username } = inputState;
  const setErrorData = useAlertStore((state) => state.setErrorData);
  function handleInput({
    target: { name, value },
  }: inputHandlerEventType): void {
    setInputState((prev) => ({ ...prev, [name]: value }));
  }

  const { mutate } = useLoginUser();

  function signIn() {
    const user: LoginType = {
      username: username,
      password: password,
    };

    mutate(user, {
      onSuccess: (res) => {
        login(res.access_token, "login", res.refresh_token);
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
    <div className="flex h-full w-full flex-col items-center justify-center bg-muted">
      <div className="flex w-72 flex-col items-center justify-center gap-2">
        <img
          src="https://scontent-arn2-1.xx.fbcdn.net/v/t39.30808-6/499498872_122132145854766980_5268724011023190696_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=u5dFev5AG-kQ7kNvwFS6K3m&_nc_oc=AdltILxg_X65VXBn-MK3Z58PgtgR7ITbbYcGrvZSWDnQLiIitDDiDq9uw1DoamQT61U&_nc_zt=23&_nc_ht=scontent-arn2-1.xx&_nc_gid=mpLb2UFdGIvVDUjGf2bZuw&oh=00_AfXfUa1TAFSuNwQPVCsbeshZuHKq0TqnRwUgl4EdrFju9w&oe=68A94B99"
          alt="Axie Studio logo"
          className="h-10 w-10 scale-[1.5] rounded object-contain"
        />
        <span className="mb-6 text-2xl font-semibold text-primary">Admin</span>
        <Input
          onChange={({ target: { value } }) => {
            handleInput({ target: { name: "username", value } });
          }}
          className="bg-background"
          placeholder="Username"
        />
        <Input
          type="password"
          onChange={({ target: { value } }) => {
            handleInput({ target: { name: "password", value } });
          }}
          className="bg-background"
          placeholder="Password"
        />
        <Button
          onClick={() => {
            signIn();
          }}
          variant="default"
          className="w-full"
        >
          Login
        </Button>
      </div>
    </div>
  );
}
