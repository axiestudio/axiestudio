import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface ReactivateResponse {
  status: string;
  message: string;
  subscription_end?: string;
}

export const useReactivateSubscription: useMutationFunctionType<
  undefined,
  undefined
> = (options?) => {
  const { mutate } = UseRequestProcessor();

  const reactivateSubscriptionFn = async (): Promise<ReactivateResponse> => {
    const res = await api.post(`${getURL("SUBSCRIPTIONS")}/reactivate`);
    return res.data;
  };

  const mutation = mutate(["useReactivateSubscription"], reactivateSubscriptionFn, options);

  return mutation;
};
