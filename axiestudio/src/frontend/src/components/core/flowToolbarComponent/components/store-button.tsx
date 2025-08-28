import { useState } from "react";
import { Button } from "@/components/ui/button";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
// import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { useStoreStore } from "@/stores/storeStore";
import { ENABLE_AXIESTUDIO_STORE } from "@/customization/feature-flags";

export default function StoreButton() {
  const hasStore = useStoreStore((state) => state.hasStore);
  const [isHovered, setIsHovered] = useState(false);

  // Don't show if store is not enabled
  if (!ENABLE_AXIESTUDIO_STORE || !hasStore) {
    return null;
  }

  const handleStoreClick = () => {
    // Open store in new tab to keep current flow open
    window.open("/axiestudio-store", "_blank");
  };

  return (
    <ShadTooltip content="Bläddra i Store - Hitta fantastiska flöden och komponenter!" side="bottom">
      <Button
        variant="ghost"
        size="sm"
        onClick={handleStoreClick}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="h-9 px-3 text-muted-foreground hover:text-foreground hover:bg-accent transition-all duration-200"
      >
        <ForwardedIconComponent
          name="ShoppingBag"
          className={`h-4 w-4 mr-2 transition-transform duration-200 ${isHovered ? 'scale-110' : ''}`}
        />
        <span className="text-sm font-medium">Store</span>
      </Button>
    </ShadTooltip>
  );
}
