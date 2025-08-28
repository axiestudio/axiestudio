import ForwardedIconComponent from "@/components/common/genericIconComponent";
import CardsWrapComponent from "@/components/core/cardsWrapComponent";
import { Button } from "@/components/ui/button";
import { useFolderStore } from "@/stores/foldersStore";
import useFileDrop from "../../hooks/use-on-file-drop";

type EmptyPageProps = {
  setOpenModal: (open: boolean) => void;
};

export const EmptyPage = ({ setOpenModal }: EmptyPageProps) => {
  const folders = useFolderStore((state) => state.folders);
  const handleFileDrop = useFileDrop(undefined);

  return (
    <CardsWrapComponent
      dragMessage={`Släpp dina flöden eller komponenter här`}
      onFileDrop={handleFileDrop}
    >
      <div className="m-0 h-full w-full bg-gradient-to-br from-background via-background to-muted/20 p-0">
        <div className="text-container">
          <div className="relative z-20 flex w-full flex-col items-center justify-center gap-8">
            <div className="flex flex-col items-center gap-6">
              <div className="rounded-2xl bg-card/60 backdrop-blur-sm border border-border/30 p-4 shadow-lg">
                <img
                  src="/logo192.png"
                  alt="Axie Studio Logo"
                  className="h-8 w-8 object-contain rounded"
                />
              </div>
              <div className="text-center space-y-3">
                <h1
                  className="text-3xl font-light text-foreground tracking-tight"
                  data-testid="mainpage_title"
                >
                  {folders?.length > 1 ? "Tomt projekt" : "Välkommen till Axie Studio"}
                </h1>
                <p
                  data-testid="empty-project-description"
                  className="text-base text-muted-foreground max-w-md"
                >
                  Skapa kraftfulla AI-arbetsflöden med vår visuella flödesbyggare. Börja med en mall eller bygg från grunden.
                </p>
              </div>
            </div>
            <Button
              onClick={() => setOpenModal(true)}
              id="new-project-btn"
              data-testid="new_project_btn_empty_page"
              className="h-12 px-8 bg-primary hover:bg-primary/90 text-primary-foreground font-medium text-base shadow-lg hover:shadow-xl transition-all duration-200"
            >
              Skapa nytt flöde
            </Button>
          </div>
        </div>
        <div className="gradient-bg">
          <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
            <defs>
              <filter id="lf-balls">
                <feGaussianBlur
                  in="turbulence"
                  stdDeviation="10"
                  result="blur"
                />
                <feColorMatrix
                  in="blur"
                  type="matrix"
                  values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
                  result="color-matrix"
                />
                <feBlend in="SourceGraphic" in2="color-matrix" mode="normal" />
              </filter>
              <filter id="lf-noise">
                <feTurbulence
                  type="fractalNoise"
                  baseFrequency="0.65"
                  stitchTiles="stitch"
                />
              </filter>
            </defs>
          </svg>
          <div className="gradients-container">
            <div className="g1" />
            <div className="g2" />
            <div className="g3" />
            <div className="g4" />
            <div className="g5" />
            <div className="g6" />
          </div>
        </div>
      </div>
    </CardsWrapComponent>
  );
};

export default EmptyPage;
