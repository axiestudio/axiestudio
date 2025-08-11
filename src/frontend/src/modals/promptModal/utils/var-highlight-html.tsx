import type { IVarHighlightType } from "../../../types/components";

function varHighlightHTML({ name }: IVarHighlightType): string {
  const html = `<span class="chat-message-highlight">{${name}}</span>`;
  return html;
}


export default varHighlightHTML;
export { varHighlightHTML };