import type { CustomCellRendererProps } from "ag-grid-react";
import { RenderIcons } from "@/components/common/renderIconComponent";

function CellRenderShortcuts(params: CustomCellRendererProps) {
  const shortcut = params.value;
  const splitShortcut = shortcut?.split("+");
  return <RenderIcons filteredShortcut={splitShortcut } tableRender />;
}


export default CellRenderShortcuts;
export { CellRenderShortcuts };