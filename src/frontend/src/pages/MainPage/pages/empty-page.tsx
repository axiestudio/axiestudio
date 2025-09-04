import { useShallow } from "zustand/react/shallow";
import logoLightSvg from "@/assets/logo_light.svg";
import logoDarkSvg from "@/assets/logo_dark.svg";
import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import CardsWrapComponent from "@/components/core/cardsWrapComponent";
import { Button } from "@/components/ui/button";
import { DotBackgroundDemo } from "@/components/ui/dot-background";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { track } from "@/customization/utils/analytics";
import { useGetTutorialQuery } from "@/controllers/API/queries/flows/use-get-tutorial";
import useAddFlow from "@/hooks/flows/use-add-flow";
import useFlowsManagerStore from "@/stores/flowsManagerStore";
import { useFolderStore } from "@/stores/foldersStore";
import useFileDrop from "../hooks/use-on-file-drop";

const EMPTY_PAGE_TITLE = "Välkommen till Axie Studio";
const EMPTY_PAGE_DESCRIPTION = "Ditt nya favoritverktyg för att leverera Agenter";
const EMPTY_PAGE_DRAG_AND_DROP_TEXT =
  "Har du redan ett flöde? Dra och släpp för att ladda upp.";
const EMPTY_PAGE_FOLDER_DESCRIPTION = "Tom mapp";
const EMPTY_PAGE_CREATE_FIRST_FLOW_BUTTON_TEXT = "Skapa första flödet";

export const EmptyPageCommunity = ({
  setOpenModal,
}: {
  setOpenModal: (open: boolean) => void;
}) => {
  const handleFileDrop = useFileDrop(undefined);
  const folders = useFolderStore((state) => state.folders);
  const navigate = useCustomNavigate();
  const addFlow = useAddFlow();
  const setCurrentFlow = useFlowsManagerStore((state) => state.setCurrentFlow);

  const { data: tutorialFlow } = useGetTutorialQuery({});

  const handleStartTutorial = async () => {
    if (tutorialFlow) {
      // Create a new flow based on the tutorial
      const newFlowId = await addFlow();

      // Set the tutorial flow as the current flow
      const tutorialFlowCopy = {
        ...tutorialFlow,
        id: newFlowId as string,
        name: `${tutorialFlow.name} - Kopia`,
      };

      setCurrentFlow(tutorialFlowCopy);

      // Navigate to the new flow
      navigate(`/flow/${newFlowId}`);

      // Track the tutorial start
      track("Tutorial Started", {
        tutorial_name: tutorialFlow.name,
        source: "empty_page"
      });
    }
  };

  return (
    <DotBackgroundDemo>
      <CardsWrapComponent
        dragMessage={`Släpp dina flöden eller komponenter här`}
        onFileDrop={handleFileDrop}
      >
        <div className="m-0 h-full w-full bg-background p-0">
          <div className="z-50 flex h-full w-full flex-col items-center justify-center gap-5">
            <div className="z-50 flex flex-col items-center gap-2">
              <div className="z-50 dark:hidden">
                <img
                  src={logoLightSvg}
                  alt="Axie Studio Logo Light"
                  data-testid="empty_page_logo_light"
                  className="relative top-3 w-32 h-32 object-contain rounded-lg"
                />
              </div>
              <div className="z-50 hidden dark:block">
                <img
                  src={logoDarkSvg}
                  alt="Axie Studio Logo Dark"
                  data-testid="empty_page_logo_dark"
                  className="relative top-3 w-32 h-32 object-contain rounded-lg"
                />
              </div>
              <span
                data-testid="mainpage_title"
                className="z-50 text-center font-chivo text-2xl font-medium text-foreground"
              >
                {EMPTY_PAGE_TITLE}
              </span>

              <span
                data-testid="empty_page_description"
                className="z-50 text-center text-base text-secondary-foreground"
              >
                {folders?.length > 1
                  ? EMPTY_PAGE_FOLDER_DESCRIPTION
                  : EMPTY_PAGE_DESCRIPTION}
              </span>
            </div>

            <div className="flex w-full max-w-[510px] flex-col gap-7 sm:gap-[29px]">
              <Button
                className="group mx-3 h-[84px] sm:mx-0"
                onClick={() => setOpenModal(true)}
                data-testid="empty_page_create_flow_button"
              >
                <div className="relative flex flex-col rounded-lg border-[1px] bg-background p-4 transition-all duration-300 hover:border-accent-pink-foreground">
                  <div className="grid w-full items-center justify-between gap-2">
                    <div className="flex gap-3">
                      <ForwardedIconComponent name="Plus" className="h-6 w-6" />
                      <div>
                        <span className="font-semibold">Skapa Nytt Flöde</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-base text-secondary-foreground">
                        Börja bygga din AI-applikation med Axie Studio
                      </span>
                    </div>
                  </div>
                </div>
              </Button>

              {tutorialFlow && (
                <Button
                  className="group mx-3 h-[84px] sm:mx-0"
                  onClick={handleStartTutorial}
                  data-testid="empty_page_tutorial_button"
                >
                  <div className="relative flex flex-col rounded-lg border-[1px] bg-background p-4 transition-all duration-300 hover:border-primary">
                    <div className="grid w-full items-center justify-between gap-2">
                      <div className="flex gap-3">
                        <ForwardedIconComponent name="GraduationCap" className="h-6 w-6 text-primary" />
                        <div>
                          <span className="font-semibold">🎓 Starta Tutorial</span>
                        </div>
                      </div>
                      <div>
                        <span className="text-base text-secondary-foreground">
                          Lär dig Axie Studio steg för steg (15-20 min)
                        </span>
                      </div>
                    </div>
                  </div>
                </Button>
              )}

              <Button
                className="group mx-3 h-[84px] sm:mx-0"
                onClick={() => window.open("https://www.axiestudio.se", "_blank", "noopener,noreferrer")}
                data-testid="empty_page_documentation_button"
              >
                <div className="relative flex flex-col rounded-lg border-[1px] bg-background p-4 transition-all duration-300 hover:border-accent-pink-foreground">
                  <div className="grid w-full items-center justify-between gap-2">
                    <div className="flex gap-3">
                      <ForwardedIconComponent name="BookOpen" className="h-6 w-6" />
                      <div>
                        <span className="font-semibold">Dokumentation</span>
                      </div>
                    </div>
                    <div>
                      <span className="text-base text-secondary-foreground">
                        Lär dig hur du bygger kraftfulla AI-applikationer
                      </span>
                    </div>
                  </div>
                </div>
              </Button>

              <Button
                variant="default"
                className="z-10 m-auto mt-3 h-10 w-full max-w-[10rem] rounded-lg font-bold transition-all duration-300"
                onClick={() => setOpenModal(true)}
                id="new-project-btn"
                data-testid="new_project_btn_empty_page"
              >
                <ForwardedIconComponent
                  name="Plus"
                  aria-hidden="true"
                  className="h-4 w-4"
                />
                <span>{EMPTY_PAGE_CREATE_FIRST_FLOW_BUTTON_TEXT}</span>
              </Button>
            </div>
          </div>
        </div>
        <p
          data-testid="empty_page_drag_and_drop_text"
          className="absolute bottom-5 left-0 right-0 mt-4 cursor-default text-center text-xxs text-muted-foreground"
        >
          {EMPTY_PAGE_DRAG_AND_DROP_TEXT}
        </p>
      </CardsWrapComponent>
    </DotBackgroundDemo>
  );
};

export default EmptyPageCommunity;
