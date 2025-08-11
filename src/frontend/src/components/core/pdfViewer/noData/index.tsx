import { PDFErrorTitle, PDFLoadError } from "../../../../constants/constants";

function NoDataPdf(): JSX.Element {
  return (
    <div className="flex h-full w-full flex-col items-center justify-center bg-muted">
      <div className="chat-alert-box">
        <span>
          📄 <span className="axiestudio-chat-span">{PDFErrorTitle}</span>
        </span>
        <br />
        <div className="axiestudio-chat-desc">
          <span className="axiestudio-chat-desc-span">{PDFLoadError} </span>
        </div>
      </div>
    </div>
  );
}


export default NoDataPdf;
export { NoDataPdf };