import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface CreateCheckoutRequest {
  success_url: string;
  cancel_url: string;
}

interface CheckoutResponse {
  checkout_url: string;
}

export const useCreateCheckout: useMutationFunctionType<
  undefined,
  CreateCheckoutRequest
> = (options?) => {
  const { mutate } = UseRequestProcessor();

  const createCheckoutFn = async (
    request: CreateCheckoutRequest
  ): Promise<CheckoutResponse> => {
    const res = await api.post(`${getURL("SUBSCRIPTIONS")}/create-checkout`, request);
    return res.data;
  };

  const mutation = mutate(["useCreateCheckout"], createCheckoutFn, options);

  return mutation;
};
