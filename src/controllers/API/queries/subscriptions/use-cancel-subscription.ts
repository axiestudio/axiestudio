import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface CancelResponse {
  status: string;
  message: string;
}

export const useCancelSubscription: useMutationFunctionType<
  undefined,
  undefined
> = (options?) => {
  const { mutate } = UseRequestProcessor();

  const cancelSubscriptionFn = async (): Promise<CancelResponse> => {
    const res = await api.delete(`${getURL("SUBSCRIPTIONS")}/cancel`);
    return res.data;
  };

  const mutation = mutate(["useCancelSubscription"], cancelSubscriptionFn, options);

  return mutation;
};
