import { OPENAI_VOICES } from "@/constants/constants";
import IconComponent from "../../../../../../../../../../components/common/genericIconComponent";
import ShadTooltip from "../../../../../../../../../../components/common/shadTooltipComponent";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../../../../../../../../../components/ui/select";
import { toTitleCase } from "../../../../../../../../../../utils/utils";

interface VoiceSelectProps {
  voice: string;
  handleSetVoice: (value: string) => void;
  allVoices: { value: string; name: string }[];
}

const VoiceSelect = ({
  voice,
  handleSetVoice,
  allVoices,
}: VoiceSelectProps) => {
  allVoices = allVoices?.length === 0 || !allVoices ? OPENAI_VOICES : allVoices;

  return (
    <div className="grid w-full items-center gap-2">
      <span className="flex w-full items-center text-sm">
        Röst
        <ShadTooltip content="Du kan välja ElevenLabs-röster om du har en ElevenLabs API-nyckel. Annars kan du bara välja OpenAI-röster.">
          <div>
            <IconComponent
              name="Info"
              strokeWidth={2}
              className="relative -top-[3px] left-1 h-[14px] w-[14px] text-placeholder"
            />
          </div>
        </ShadTooltip>
      </span>

      <Select value={voice} onValueChange={handleSetVoice}>
        <SelectTrigger className="h-9 w-full">
          <SelectValue placeholder="Välj" />
        </SelectTrigger>
        <SelectContent className="max-h-[200px]">
          <SelectGroup>
            {allVoices?.map((voice, index) => (
              <SelectItem value={voice?.value} key={index}>
                <div className="max-w-[220px] truncate text-left">
                  {toTitleCase(voice?.name)}
                </div>
              </SelectItem>
            ))}
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>
  );
};

export default VoiceSelect;
