import { convertTestName } from "@/components/common/storeCardComponent/utils/convert-test-name";
import { Badge } from "@/components/ui/badge";
import { nodeColorsName } from "@/utils/styleUtils";

export default function HandleTooltipComponent({
  isInput,
  tooltipTitle,
  isConnecting,
  isCompatible,
  isSameNode,
  left,
}: {
  isInput: boolean;
  tooltipTitle: string;
  isConnecting: boolean;
  isCompatible: boolean;
  isSameNode: boolean;
  left: boolean;
}) {
  const tooltips = tooltipTitle.split("\n");
  const plural = tooltips.length > 1 ? "s" : "";

  return (
    <div className="font-medium">
      {isSameNode ? (
        "Kan inte ansluta till samma nod"
      ) : (
        <div className="flex items-center gap-1.5">
          {isConnecting ? (
            isCompatible ? (
              <span>
                <span className="font-semibold">Anslut</span> till
              </span>
            ) : (
              <span>Inkompatibel med</span>
            )
          ) : (
            <span className="text-xs">
              {isInput
                ? `Inmatningstyp${plural === "s" ? "er" : ""}`
                : `Utmatningstyp${plural === "s" ? "er" : ""}`}
              :{" "}
            </span>
          )}
          {tooltips.map((word, index) => (
            <Badge
              className="h-6 rounded-md p-1"
              key={`${index}-${word.toLowerCase()}`}
              style={{
                backgroundColor: left
                  ? `hsl(var(--datatype-${nodeColorsName[word]}))`
                  : `hsl(var(--datatype-${nodeColorsName[word]}-foreground))`,
                color: left
                  ? `hsl(var(--datatype-${nodeColorsName[word]}-foreground))`
                  : `hsl(var(--datatype-${nodeColorsName[word]}))`,
              }}
              data-testid={`${isInput ? "input" : "output"}-tooltip-${convertTestName(word)}`}
            >
              {word}
            </Badge>
          ))}
          {isConnecting && <span>{isInput ? `inmatning` : `utmatning`}</span>}
        </div>
      )}
      {!isConnecting && (
        <div className="mt-2 flex flex-col gap-0.5 text-xs leading-6">
          <div>
            <b>Dra</b> för att ansluta kompatibla {!isInput ? "inmatningar" : "utmatningar"}
          </div>
          <div>
            <b>Klicka</b> för att filtrera kompatibla {!isInput ? "inmatningar" : "utmatningar"}{" "}
            och komponenter
          </div>
        </div>
      )}
    </div>
  );
}
