import { useTranslation } from "react-i18next";
const NoResultsMessage = ({
  onClearSearch,
  message = t("flows.nocomponentsfound"),
  clearSearchText = t("common.clearyoursearch"),
  additionalText = "or filter and try a different query.",
}) => {
  const { t } = useTranslation();
  return (
    <div className="flex h-full flex-col items-center justify-center p-3 text-center">
      <p className="text-sm text-secondary-foreground">
        {message}{" "}
        <a
          className="cursor-pointer underline underline-offset-4"
          onClick={onClearSearch}
        >
          {clearSearchText}
        </a>{" "}
        {additionalText}
      </p>
    </div>
  );
};

export default NoResultsMessage;

export { NoResultsMessage };