from axiestudio.schema.table import EditMode

TOOL_OUTPUT_NAME = "component_as_tool"
TOOL_OUTPUT_DISPLAY_NAME = "Verktygsuppsättning"
TOOLS_METADATA_INPUT_NAME = "tools_metadata"
TOOL_TABLE_SCHEMA = [
    {
        "name": "name",
        "display_name": "Verktygsnamn",
        "type": "str",
        "description": "Ange namnet på verktyget.",
        "sortable": False,
        "filterable": False,
        "edit_mode": EditMode.INLINE,
        "hidden": False,
    },
    {
        "name": "description",
        "display_name": "Verktygsbeskrivning",
        "type": "str",
        "description": "Beskriv syftet med verktyget.",
        "sortable": False,
        "filterable": False,
        "edit_mode": EditMode.POPOVER,
        "hidden": False,
    },
    {
        "name": "tags",
        "display_name": "Tool Identifiers",
        "type": "str",
        "description": ("The default identifiers for the tools and cannot be changed."),
        "disable_edit": True,
        "sortable": False,
        "filterable": False,
        "edit_mode": EditMode.INLINE,
        "hidden": True,
    },
    {
        "name": "status",
        "display_name": "Enable",
        "type": "boolean",
        "description": "Indicates whether the tool is currently active. Set to True to activate this tool.",
        "default": True,
    },
]

TOOLS_METADATA_INFO = "Modify tool names and descriptions to help agents understand when to use each tool."

TOOL_UPDATE_CONSTANTS = ["tool_mode", "tool_actions", TOOLS_METADATA_INPUT_NAME, "flow_name_selected"]
