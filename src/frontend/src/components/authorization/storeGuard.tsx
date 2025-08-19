import { ReactNode } from "react";
import { ENABLE_AXIESTUDIO_STORE } from "@/customization/feature-flags";

interface StoreGuardProps {
  children: ReactNode;
}

export function StoreGuard({ children }: StoreGuardProps) {
  // If store is not enabled, don't render the children
  if (!ENABLE_AXIESTUDIO_STORE) {
    return null;
  }

  return <>{children}</>;
}

export default StoreGuard;
