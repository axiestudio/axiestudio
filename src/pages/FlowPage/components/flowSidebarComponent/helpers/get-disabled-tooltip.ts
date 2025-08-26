import type { UniqueInputsComponents } from "../types";

export const getDisabledTooltip = (
  SBItemName: string,
  uniqueInputsComponents: UniqueInputsComponents,
) => {
  if (SBItemName === "ChatInput" && uniqueInputsComponents.chatInput) {
    return "Chattinmatning redan tillagd";
  }
  if (SBItemName === "Webhook" && uniqueInputsComponents.webhookInput) {
    return "Webhook redan tillagd";
  }
  return "";
};
