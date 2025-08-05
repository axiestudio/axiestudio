import { Cookies } from "react-cookie";
import { AXIESTUDIO_ACCESS_TOKEN } from "@/constants/constants";

export const customGetAccessToken = () => {
  const cookies = new Cookies();
  return cookies.get(AXIESTUDIO_ACCESS_TOKEN);
};
