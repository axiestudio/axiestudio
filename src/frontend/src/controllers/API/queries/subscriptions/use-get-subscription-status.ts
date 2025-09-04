import { useQueryFunctionType } from "@/types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface SubscriptionStatus {
  subscription_status: string;
  subscription_id: string | null;
  trial_start: string | null;
  trial_end: string | null;
  trial_expired: boolean;
  trial_days_left: number | null;
  subscription_start: string | null;
  subscription_end: string | null;
  has_stripe_customer: boolean;
  is_superuser?: boolean;
}

export const useGetSubscriptionStatus: useQueryFunctionType<
  undefined,
  SubscriptionStatus
> = (options?) => {
  const { query } = UseRequestProcessor();

  const getSubscriptionStatusFn = async (): Promise<SubscriptionStatus> => {
    const res = await api.get(`${getURL("SUBSCRIPTIONS")}/status`);
    return res.data;
  };

  const queryResult = query(
    ["useGetSubscriptionStatus"],
    getSubscriptionStatusFn,
    options
  );

  return queryResult;
};
