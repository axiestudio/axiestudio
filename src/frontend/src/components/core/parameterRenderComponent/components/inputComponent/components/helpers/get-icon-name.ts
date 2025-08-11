export const getIconName = (
  t: (key: string) => string,
  disabled?: boolean,
  selectedOption?: string,
  optionsIcon?: string,
  nodeStyle?: boolean,
  isToolMode?: boolean,
) => {
  if (isToolMode) return t("common.hammer");
  if (disabled) return "lock";
  if (selectedOption && nodeStyle) return t("common.globeokicon");
  return optionsIcon;
};
