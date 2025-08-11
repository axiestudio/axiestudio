import type { APITemplateType } from "../../types/api";

function getFieldTitle(
  template: APITemplateType,
  templateField: string,
): string {
  return template[templateField].display_name
    ? template[templateField].display_name!
    : (template[templateField].name ?? templateField);
}


export default getFieldTitle;
export { getFieldTitle };