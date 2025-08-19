import { ReactNode } from "react";
import { CustomNavigate } from "@/customization/components/custom-navigate";
import { useStoreStore } from "../../../stores/storeStore";

interface StoreGuardProps {
  children: ReactNode;
}

export const StoreGuard = ({ children }: StoreGuardProps) => {
  const hasStore = useStoreStore((state) => state.hasStore);

  if (!hasStore) {
    return <CustomNavigate to="/all" replace />;
  }

  return children;
};
