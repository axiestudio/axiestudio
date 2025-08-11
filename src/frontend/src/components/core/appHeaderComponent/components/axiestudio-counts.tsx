import ShadTooltip from "@/components/common/shadTooltipComponent";

import { useTranslation } from "react-i18next";

export const AxieStudioCounts = () => {
  const { t } = useTranslation();

  return (
    <div className="flex items-center gap-2">
      <ShadTooltip
        content="Axie Studio"
        side="bottom"
        styleClasses="z-10"
      >
        <div className="hit-area-hover flex items-center gap-2 rounded-md p-1 text-muted-foreground">
          <span className="text-xs font-semibold">{t("common.axiestudio")}</span>
        </div>
      </ShadTooltip>
    </div>
  );
};

export default AxieStudioCounts;
