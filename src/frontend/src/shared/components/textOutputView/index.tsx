import { Textarea } from "../../../components/ui/textarea";

import { useTranslation } from "react-i18next";
const TextOutputView = ({
  left,
  value,
}: {
  left: boolean | undefined;
  value: any;
}) => {
  const { t } = useTranslation(); if (typeof value === "object" && Object.keys(value).includes("text")) {
    value = value.text;
   }

  const isTruncated = value?.length > 20000;

  return (
    <>
      {" "}
      <Textarea
        className={`w-full resize-none custom-scroll ${left ? "min-h-32" : "h-full"}`}
        placeholder={"Empty"}
        readOnly
        value={value}
      />
      {isTruncated && (
        <div className="mt-2 text-xs text-muted-foreground">{t("greetings.thisoutputhasbeen")}</div>
      )}
    </>
  );
};

export default TextOutputView;

export { TextOutputView };