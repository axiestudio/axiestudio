import type { useQueryFunctionType } from "@/types/api";
import type { FlowType } from "@/types/flow";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

export const useGetTutorialQuery: useQueryFunctionType<
  undefined,
  FlowType | null
> = (options) => {
  const { query } = UseRequestProcessor();

  const getTutorialFn = async () => {
    return await api.get<FlowType | null>(`${getURL("TUTORIAL")}/`);
  };

  const responseFn = async () => {
    const { data } = await getTutorialFn();
    return data;
  };

  const queryResult = query(["useGetTutorialQuery"], responseFn, {
    ...options,
    retry: 3,
  });

  return queryResult;
};
