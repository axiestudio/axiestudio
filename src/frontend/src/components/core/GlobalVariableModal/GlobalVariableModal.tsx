import { useEffect, useState } from "react";
import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs-button";
import { useGetTypes } from "@/controllers/API/queries/flows/use-get-types";
import {
  useGetGlobalVariables,
  usePatchGlobalVariables,
  usePostGlobalVariables,
} from "@/controllers/API/queries/variables";
import BaseModal from "@/modals/baseModal";
import useAlertStore from "@/stores/alertStore";
import getUnavailableFields from "@/stores/globalVariablesStore/utils/get-unavailable-fields";
import { useTypesStore } from "@/stores/typesStore";
import type { ResponseErrorDetailAPI } from "@/types/api";
import type { GlobalVariable } from "@/types/global_variables";
import InputComponent from "../parameterRenderComponent/components/inputComponent";
import sortByName from "./utils/sort-by-name";

//TODO IMPLEMENT FORM LOGIC

export default function GlobalVariableModal({
  children,
  asChild,
  initialData,
  referenceField,
  open: myOpen,
  setOpen: mySetOpen,
  disabled = false,
}: {
  children?: JSX.Element;
  asChild?: boolean;
  initialData?: GlobalVariable;
  referenceField?: string;
  open?: boolean;
  setOpen?: (a: boolean | ((o?: boolean) => boolean)) => void;
  disabled?: boolean;
}): JSX.Element {
  const [key, setKey] = useState(initialData?.name ?? "");
  const [value, setValue] = useState(initialData?.value ?? "");
  const [type, setType] = useState(initialData?.type ?? "Credential");
  const [fields, setFields] = useState<string[]>(
    initialData?.default_fields ?? [],
  );
  const [open, setOpen] =
    mySetOpen !== undefined && myOpen !== undefined
      ? [myOpen, mySetOpen]
      : useState(false);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const componentFields = useTypesStore((state) => state.ComponentFields);
  const { mutate: mutateAddGlobalVariable } = usePostGlobalVariables();
  const { mutate: updateVariable } = usePatchGlobalVariables();
  const { data: globalVariables } = useGetGlobalVariables();
  const [availableFields, setAvailableFields] = useState<string[]>([]);
  useGetTypes({ checkCache: true, enabled: !!globalVariables });

  useEffect(() => {
    if (globalVariables && componentFields.size > 0) {
      const unavailableFields = getUnavailableFields(globalVariables);
      const fields = Array.from(componentFields).filter(
        (field) => !Object.hasOwn(unavailableFields, field.trim()),
      );
      setAvailableFields(
        sortByName(fields.concat(initialData?.default_fields ?? [])),
      );
      if (referenceField && fields.includes(referenceField)) {
        setFields([referenceField]);
      }
    } else {
      setAvailableFields(["System", "Systemmeddelande", "Systemprompt"]);
    }
  }, [globalVariables, componentFields, initialData]);

  const setSuccessData = useAlertStore((state) => state.setSuccessData);

  function handleSaveVariable() {
    const data: {
      name: string;
      value: string;
      type?: string;
      default_fields?: string[];
    } = {
      name: key,
      type,
      value,
      default_fields: fields,
    };

    mutateAddGlobalVariable(data, {
      onSuccess: (res) => {
        const { name } = res;
        setKey("");
        setValue("");
        setType("");
        setFields([]);
        setOpen(false);

        setSuccessData({
          title: `Variabel ${name} ${initialData ? "uppdaterad" : "skapad"} framgångsrikt`,
        });
      },
      onError: (error) => {
        const responseError = error as ResponseErrorDetailAPI;
        setErrorData({
          title: `Fel vid ${initialData ? "uppdatering" : "skapande"} av variabel`,
          list: [
            responseError?.response?.data?.detail ??
              `Ett oväntat fel uppstod vid ${initialData ? "uppdatering av" : "skapande av"} variabel. Vänligen försök igen.`,
          ],
        });
      },
    });
  }

  function submitForm() {
    if (!initialData || !initialData.id) {
      handleSaveVariable();
    } else {
      updateVariable({
        id: initialData.id,
        name: key,
        value: value,
        default_fields: fields,
      });
      setOpen(false);
    }
  }

  return (
    <BaseModal
      open={open}
      setOpen={setOpen}
      size="x-small"
      onSubmit={submitForm}
      disable={disabled}
    >
      <BaseModal.Header description="Denna variabel kommer att vara tillgänglig för användning i alla dina flöden.">
        <ForwardedIconComponent
          name="Globe"
          className="h-6 w-6 pr-1 text-primary"
          aria-hidden="true"
        />
        {initialData ? "Uppdatera Variabel" : "Skapa Variabel"}
      </BaseModal.Header>
      <BaseModal.Trigger disable={disabled} asChild={asChild}>
        {children}
      </BaseModal.Trigger>
      <BaseModal.Content>
        <div className="flex h-full w-full flex-col gap-4">
          <div className="space-y-2">
            <Label>Typ*</Label>
            <Tabs
              defaultValue={type}
              onValueChange={setType}
              className="w-full"
            >
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger
                  disabled={!!initialData?.type}
                  data-testid="credential-tab"
                  value="Credential"
                >
                  Autentisering
                </TabsTrigger>
                <TabsTrigger
                  disabled={!!initialData?.type}
                  data-testid="generic-tab"
                  value="Generic"
                >
                  Allmän
                </TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          <div className="space-y-2" id="global-variable-modal-inputs">
            <Label>Namn*</Label>
            <Input
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="Ange ett namn för variabeln..."
            />
          </div>

          <div className="space-y-2">
            <Label>Värde*</Label>
            {type === "Credential" ? (
              <InputComponent
                password
                value={value}
                onChange={(e) => setValue(e)}
                placeholder="Ange ett värde för variabeln..."
                nodeStyle
              />
            ) : (
              <Input
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder="Enter a value for the variable..."
              />
            )}
          </div>

          <div className="space-y-2">
            <Label>Tillämpa på fält</Label>
            <InputComponent
              setSelectedOptions={(value) => setFields(value)}
              selectedOptions={fields}
              options={availableFields}
              password={false}
              placeholder="Välj ett fält för variabeln..."
              id="apply-to-fields"
              popoverWidth="29rem"
              optionsPlaceholder="Fält"
            />
            <div className="text-xs text-muted-foreground">
              Valda fält kommer automatiskt att tillämpa variabeln som standardvärde.
            </div>
          </div>
        </div>
      </BaseModal.Content>
      <BaseModal.Footer
        submit={{
          label: `${initialData ? "Uppdatera" : "Spara"} Variabel`,
          dataTestId: "save-variable-btn",
        }}
      />
    </BaseModal>
  );
}
