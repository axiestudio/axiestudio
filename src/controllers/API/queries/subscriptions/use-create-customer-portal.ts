import { useMutationFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface CustomerPortalResponse {
  portal_url: string;
}

export const useCreateCustomerPortal: useMutationFunctionType<
  undefined,
  undefined
> = (options?) => {
  const { mutate } = UseRequestProcessor();

  const createCustomerPortalFn = async (): Promise<CustomerPortalResponse> => {
    const res = await api.post(`${getURL("SUBSCRIPTIONS")}/customer-portal`);
    return res.data;
  };

  const mutation = mutate(["useCreateCustomerPortal"], createCustomerPortalFn, options);

  return mutation;
};
