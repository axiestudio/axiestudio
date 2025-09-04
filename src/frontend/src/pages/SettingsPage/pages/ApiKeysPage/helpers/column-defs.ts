import TableAutoCellRender from "@/components/core/parameterRenderComponent/components/tableComponent/components/tableAutoCellRender";

export const getColumnDefs = () => {
  return [
    {
      headerCheckboxSelection: true,
      checkboxSelection: true,
      showDisabledCheckboxes: true,
      headerName: "Namn",
      field: "name",
      cellRenderer: TableAutoCellRender,
      flex: 2,
    },
    {
      headerName: "Nyckel",
      field: "api_key",
      cellRenderer: TableAutoCellRender,
      flex: 1,
    },
    {
      headerName: "Skapad",
      field: "created_at",
      cellRenderer: TableAutoCellRender,
      flex: 1,
    },
    {
      headerName: "Senast Använd",
      field: "last_used_at",
      cellRenderer: TableAutoCellRender,
      flex: 1,
    },
    {
      headerName: "Totala Användningar",
      field: "total_uses",
      cellRenderer: TableAutoCellRender,
      flex: 1,
      resizable: false,
    },
  ];
};
