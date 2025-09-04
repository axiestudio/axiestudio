import IconComponent from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import { Button } from "@/components/ui/button";

export const AddFolderButton = ({
  onClick,
  disabled,
  loading,
}: {
  onClick: () => void;
  disabled: boolean;
  loading: boolean;
}) => (
  <ShadTooltip content="Skapa nytt projekt" styleClasses="z-50">
    <Button
      variant="ghost"
      size="icon"
      className="h-8 w-8 border border-zinc-300 text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:border-zinc-600 dark:text-zinc-300 dark:hover:bg-zinc-700 dark:hover:text-white"
      onClick={onClick}
      data-testid="add-project-button"
      disabled={disabled}
      loading={loading}
    >
      <IconComponent name="Plus" className="h-4 w-4" />
    </Button>
  </ShadTooltip>
);
