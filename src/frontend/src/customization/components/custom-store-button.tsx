import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { SidebarMenuButton } from "@/components/ui/sidebar";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { useLocation } from "react-router-dom";

export const CustomStoreButton = () => {
  const navigate = useCustomNavigate();
  const location = useLocation();
  const isAxieStudioStoreActive = location.pathname.includes("/axiestudio-store");

  return (
    <>
      <div className="flex w-full items-center" data-testid="button-store">
        <SidebarMenuButton
          size="md"
          className="text-sm"
          onClick={() => {
            window.open("/store", "_blank");
          }}
        >
          <ForwardedIconComponent name="Store" className="h-4 w-4" />
          Store
        </SidebarMenuButton>
      </div>

      <div className="flex w-full items-center" data-testid="button-axiestudio-store">
        <SidebarMenuButton
          size="md"
          className="text-sm"
          isActive={isAxieStudioStoreActive}
          onClick={() => {
            navigate("/axiestudio-store");
          }}
        >
          <ForwardedIconComponent name="Package" className="h-4 w-4" />
          AxieStudio Store
        </SidebarMenuButton>
      </div>
    </>
  );
};
