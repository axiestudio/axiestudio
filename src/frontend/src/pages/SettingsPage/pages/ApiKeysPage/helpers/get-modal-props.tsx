import { useTranslation } from "react-i18next";
export const getModalPropsApiKey = () => { const modalProps = {
    title: t("actions.createapikey"),
    description: t("actions.createasecretapi"),
    inputPlaceholder: t("common.myapikey"),
    buttonText: t("common.generateapikey"),
    generatedKeyMessage: (
      <>
        {" " }
        Please save this secret key somewhere safe and accessible. For security
        reasons, <strong>you won't be able to view it again</strong> through
        your account. If you lose this secret key, you'll need to generate a new
        one.
      </>
    ),
    showIcon: true,
    inputLabel: (
      <>
        <span className="text-sm">Description</span>{" "}
        <span className="text-xs text-muted-foreground">(optional)</span>
      </>
    ),
  };

  return modalProps;
};
