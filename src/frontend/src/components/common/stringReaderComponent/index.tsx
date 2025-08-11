import TextModal from "../../../modals/textModal";

function StringReader({
  string,
  setValue,
  editable = false,
}: {
  string: string | null;
  setValue: (value: string) => void;
  editable: boolean;
}): JSX.Element {
  return (
    <TextModal editable={editable} setValue={setValue} value={string ?? ""}>
      {/* INVISIBLE CHARACTER TO PREVENT AGgrid bug */}
      <span className="truncate">{string ?? "‎"}</span>
    </TextModal>
  );
}


export default StringReader;
export { StringReader };