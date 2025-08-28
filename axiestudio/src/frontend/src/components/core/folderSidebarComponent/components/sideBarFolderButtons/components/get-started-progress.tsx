import { type FC, useState } from "react";
import IconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";
import ModalsComponent from "@/pages/MainPage/components/modalsComponent";
import useFlowsManagerStore from "@/stores/flowsManagerStore";
import type { Users } from "@/types/api";

export const GetStartedProgress: FC<{
  userData: Users;
  handleDismissDialog: () => void;
}> = ({ handleDismissDialog }) => {
  const [newProjectModal, setNewProjectModal] = useState(false);

  const flows = useFlowsManagerStore((state) => state.flows);
  const hasFlows = flows && flows?.length > 0;
  const percentageGetStarted = hasFlows ? 100 : 0;

  return (
    <div className="mt-3 w-full rounded-xl bg-card/30 border border-border/40 p-4">
      <div className="mb-3 flex items-center justify-between">
        <span
          className="text-sm font-medium text-foreground"
          data-testid="get_started_progress_title"
        >
          {percentageGetStarted >= 100 ? "Complete" : "Get started"}
        </span>
        <button
          onClick={() => handleDismissDialog()}
          className="text-muted-foreground hover:text-foreground transition-colors duration-200 rounded-md p-1 hover:bg-muted/50"
          data-testid="close_get_started_dialog"
        >
          <IconComponent name="X" className="h-3 w-3" />
        </button>
      </div>

      <div className="mb-1 mt-3 flex items-center justify-between gap-3">
        <div className="h-2 w-full rounded-full bg-muted/60 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-primary/80 to-primary transition-all duration-500 ease-out"
            style={{ width: `${percentageGetStarted}%` }}
          />
        </div>
        <span
          className="text-xs font-medium text-muted-foreground min-w-[32px] text-right"
          data-testid="get_started_progress_percentage"
        >
          {percentageGetStarted}%
        </span>
      </div>

      <div className="mt-5">
        {!hasFlows && (
          <Button
            onClick={() => setNewProjectModal(true)}
            className="w-full h-10 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 hover:border-primary/30 transition-all duration-200"
            data-testid="create_flow_btn_get_started"
          >
            <span className="text-sm font-medium">
              Create your first flow
            </span>
          </Button>
        )}
        {hasFlows && (
          <div className="flex items-center justify-center gap-2 rounded-lg p-3 bg-muted/30 border border-border/30">
            <div className="h-2 w-2 rounded-full bg-emerald-500"></div>
            <span className="text-sm text-muted-foreground">
              Flow created successfully
            </span>
          </div>
        )}
      </div>

      <ModalsComponent
        openModal={newProjectModal}
        setOpenModal={setNewProjectModal}
        openDeleteFolderModal={false}
        setOpenDeleteFolderModal={() => {}}
        handleDeleteFolder={() => {}}
      />
    </div>
  );
};
