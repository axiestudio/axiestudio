import { useTranslation } from "react-i18next";
import type { CustomCellEditorProps } from "ag-grid-react";
import InputComponent from "../../../inputComponent";

function TableDropdownCellEditor({value,
  values,
  onValueChange,
  colDef,
  eGridCell,
}: CustomCellEditorProps & { values: string[] }) {
  const { t } = useTranslation();
  return (
    <div
      style={{ width: eGridCell.clientWidth }}
      className="flex h-full items-center px-2"
    >
      <InputComponent
        setSelectedOption={(value) => onValueChange(value)}
        value={value}
        options={values}
        password={false}
        placeholder={t("common.selectAnOption")}
        id="apply-to-fields"
      />
    </div>
  );
}


export default TableDropdownCellEditor;
export { TableDropdownCellEditor };