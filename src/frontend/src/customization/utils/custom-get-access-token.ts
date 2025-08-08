import { Cookies } from "react-cookie";
import { AXIESTUDIO_ACCESS_TOKEN } from "@/constants/constants";
import { getAuthCookie } from "@/utils/utils";

export const customGetAccessToken = () => {
  const cookies = new Cookies();
  return getAuthCookie(cookies, AXIESTUDIO_ACCESS_TOKEN);
};
