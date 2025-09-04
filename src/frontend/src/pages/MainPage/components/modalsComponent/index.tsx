// Modals.tsx
import TemplatesModal from "@/modals/templatesModal";
import DeleteConfirmationModal from "../../../../modals/deleteConfirmationModal";

interface ModalsProps {
  openModal: boolean;
  setOpenModal: (value: boolean) => void;
  openDeleteFolderModal: boolean;
  setOpenDeleteFolderModal: (value: boolean) => void;
  handleDeleteFolder: () => void;
}

const ModalsComponent = ({
  openModal = false,
  setOpenModal = () => {},
  openDeleteFolderModal = false,
  setOpenDeleteFolderModal = () => {},
  handleDeleteFolder = () => {},
}: ModalsProps) => (
  <>
    {openModal && <TemplatesModal open={openModal} setOpen={setOpenModal} />}
    {openDeleteFolderModal && (
      <DeleteConfirmationModal
        open={openDeleteFolderModal}
        setOpen={setOpenDeleteFolderModal}
        onConfirm={() => {
          handleDeleteFolder();
          setOpenDeleteFolderModal(false);
        }}
        description="mapp"
        note={"och alla associerade flöden och komponenter"}
      >
        <></>
      </DeleteConfirmationModal>
    )}
  </>
);

export default ModalsComponent;
