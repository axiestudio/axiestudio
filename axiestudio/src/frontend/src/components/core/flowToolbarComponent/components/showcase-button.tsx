import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";

export default function ShowcaseButton() {
  const navigate = useCustomNavigate();

  const handleShowcaseClick = () => {
    navigate("/showcase");
  };

  return (
    <ShadTooltip content="Bläddra i komponent- och flödesutställning">
      <Button
        variant="ghost"
        size="icon"
        onClick={handleShowcaseClick}
        className="h-9 w-9"
      >
        <ForwardedIconComponent
          name="Library"
          className="h-4 w-4"
        />
      </Button>
    </ShadTooltip>
  );
}
