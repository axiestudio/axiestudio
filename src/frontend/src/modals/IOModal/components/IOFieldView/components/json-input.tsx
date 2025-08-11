import { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import type { JsonEditor as VanillaJsonEditor } from "vanilla-jsoneditor";
import JsonEditor from "@/components/core/jsonEditor";
import type { IOJSONInputComponentType } from "@/types/components";
function IoJsonInput({
  value= [],
  onChange,
  left,
  output,
}: IOJSONInputComponentType): JSX.Element { const ref = useRef<any>(null);
  ref.current = value;

  const jsonEditorRef = useRef<VanillaJsonEditor | null>(null);

  useEffect(() => {
    if (jsonEditorRef.current) {
      jsonEditorRef.current.set({ json: value || { } });
    }
  }, [value]);

  return (
    <div className="h-400px w-full">
      <JsonEditor
        data={{ json: value }}
        jsonRef={jsonEditorRef}
        height="400px"
      />
    </div>
  );
}


export default IoJsonInput;
export { IoJsonInput };