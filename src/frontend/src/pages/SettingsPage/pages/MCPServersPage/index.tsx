import { useState } from "react";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import Loading from "@/components/ui/loading";
import { useDeleteMCPServer } from "@/controllers/API/queries/mcp/use-delete-mcp-server";
import { useGetMCPServer } from "@/controllers/API/queries/mcp/use-get-mcp-server";
import { useGetMCPServers } from "@/controllers/API/queries/mcp/use-get-mcp-servers";
import AddMcpServerModal from "@/modals/addMcpServerModal";
import DeleteConfirmationModal from "@/modals/deleteConfirmationModal";
import useAlertStore from "@/stores/alertStore";
import type { MCPServerInfoType } from "@/types/mcp";
import { cn } from "@/utils/utils";

export default function MCPServersPage() {
  const { data: servers } = useGetMCPServers();
  const { mutate: deleteServer } = useDeleteMCPServer();
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const [addOpen, setAddOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [editInitialData, setEditInitialData] = useState<any>(null);
  const { mutateAsync: getServer } = useGetMCPServer();
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [serverToDelete, setServerToDelete] =
    useState<MCPServerInfoType | null>(null);

  const handleEdit = async (name: string) => {
    try {
      const data = await getServer({ name });
      setEditInitialData(data);
      setEditOpen(true);
    } catch (e: any) {
      setErrorData({ title: "Fel vid hämtning av server", list: [e.message] });
    } finally {
    }
  };

  const handleDelete = (server: MCPServerInfoType) => {
    deleteServer(
      { name: server.name },
      {
        onError: (e: any) =>
          setErrorData({ title: "Fel vid borttagning av server", list: [e.message] }),
      },
    );
  };

  const openDeleteModal = (server: MCPServerInfoType) => {
    setServerToDelete(server);
    setDeleteModalOpen(true);
  };

  return (
    <div className="flex h-full w-full flex-col gap-6">
      <div className="flex w-full items-start justify-between gap-6">
        <div className="flex flex-col">
          <h2 className="flex items-center text-lg font-semibold tracking-tight">
            MCP-servrar
            <ForwardedIconComponent
              name="Mcp"
              className="ml-2 h-5 w-5 text-primary"
            />
          </h2>
          <p className="text-sm text-muted-foreground">
            Hantera MCP-servrar för användning i dina flöden.
          </p>
        </div>
        <div className="flex flex-shrink-0 items-center gap-2">
          <Button
            variant="primary"
            onClick={() => setAddOpen(true)}
            data-testid="add-mcp-server-button-page"
          >
            <ForwardedIconComponent name="Plus" className="w-4" />
            Lägg till MCP-server
          </Button>
          <AddMcpServerModal open={addOpen} setOpen={setAddOpen} />
        </div>
      </div>
      <div className="flex h-full flex-col gap-2">
        {servers ? (
          <>
            {servers.length === 0 ? (
              <div className="w-full pt-8 text-center text-sm text-muted-foreground">
                Inga MCP-servrar tillagda
              </div>
            ) : (
              <div className="text-sm font-medium text-muted-foreground">
                Tillagda MCP-servrar
              </div>
            )}
            <div className="flex flex-col gap-1">
              {servers.map((server) => (
                <div
                  key={server.id}
                  className="flex items-center justify-between rounded-lg px-3 py-2 shadow-sm transition-colors hover:bg-accent"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">{server.name}</span>
                    <ShadTooltip content={server.error}>
                      <span
                        className={cn(
                          "cursor-default select-none !text-mmd text-muted-foreground",
                          server.error && "text-accent-red-foreground",
                        )}
                      >
                        {server.toolsCount === null
                          ? server.error
                            ? server.error.startsWith("Timeout")
                              ? "Timeout"
                              : "Fel"
                            : "Laddar..."
                          : !server.toolsCount
                            ? "Inga verktyg hittades"
                            : `${server.toolsCount} verktyg`}
                      </span>
                    </ShadTooltip>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="iconSm"
                        data-testid={`mcp-server-menu-button-${server.name}`}
                        className="text-muted-foreground hover:bg-accent"
                      >
                        <ForwardedIconComponent
                          name="Ellipsis"
                          className="h-5 w-5"
                        />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleEdit(server.name)}>
                        <ForwardedIconComponent
                          name="SquarePen"
                          className="mr-2 h-4 w-4"
                        />
                        Redigera
                      </DropdownMenuItem>
                      <DropdownMenuItem
                        onClick={() => openDeleteModal(server)}
                        className="text-destructive"
                      >
                        <ForwardedIconComponent
                          name="Trash2"
                          className="mr-2 h-4 w-4"
                        />
                        Ta bort
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              ))}
            </div>
            {editOpen && (
              <AddMcpServerModal
                open={editOpen}
                setOpen={setEditOpen}
                initialData={editInitialData}
              />
            )}
            <DeleteConfirmationModal
              open={deleteModalOpen}
              setOpen={setDeleteModalOpen}
              onConfirm={() => {
                if (serverToDelete) handleDelete(serverToDelete);
                setDeleteModalOpen(false);
                setServerToDelete(null);
              }}
              description={"MCP-server"}
            />
          </>
        ) : (
          <div className="flex h-full w-full items-center justify-center">
            <Loading />
          </div>
        )}
      </div>
    </div>
  );
}
