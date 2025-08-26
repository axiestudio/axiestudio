// src/constants/constants.ts

import custom from "../customization/config-constants";
import type { languageMap } from "../types/components";

/**
 * invalid characters for flow name
 * @constant
 */
export const INVALID_CHARACTERS = [
  " ",
  ",",
  ".",
  ":",
  ";",
  "!",
  "?",
  "/",
  "\\",
  "(",
  ")",
  "[",
  "]",
  "\n",
];

/**
 * regex to highlight the variables in the text
 * @constant regexHighlight
 * @type {RegExp}
 * @default
 * @example
 * {{variable}} or {variable}
 * @returns {RegExp}
 * @description
 * This regex is used to highlight the variables in the text.
 * It matches the variables in the text that are between {{}} or {}.
 */

/**
 *  p1 – fenced code block ```...```
 *  p2 – opening brace run (one or more)
 *  p3 – variable name  (no braces)
 *  p4 – closing brace run (one or more)
 */
export const regexHighlight = /(```[\s\S]*?```)|(\{+)([^{}]+)(\}+)/g;
export const specialCharsRegex = /[!@#$%^&*()\-_=+[\]{}|;:'",.<>/?\\`´]/;

export const programmingLanguages: languageMap = {
  javascript: ".js",
  python: ".py",
  java: ".java",
  c: ".c",
  cpp: ".cpp",
  "c++": ".cpp",
  "c#": ".cs",
  ruby: ".rb",
  php: ".php",
  swift: ".swift",
  "objective-c": ".m",
  kotlin: ".kt",
  typescript: ".ts",
  go: ".go",
  perl: ".pl",
  rust: ".rs",
  scala: ".scala",
  haskell: ".hs",
  lua: ".lua",
  shell: ".sh",
  sql: ".sql",
  html: ".html",
  css: ".css",
  // add more file extensions here, make sure the key is same as language prop in CodeBlock.tsx component
};
/**
 * Number maximum of components to scroll on tooltips
 * @constant
 */
export const MAX_LENGTH_TO_SCROLL_TOOLTIP = 200;

export const MESSAGES_TABLE_ORDER = [
  "timestamp",
  "message",
  "text",
  "sender",
  "sender_name",
  "session_id",
  "files",
];

/**
 * Number maximum of components to scroll on tooltips
 * @constant
 */
export const MAX_WORDS_HIGHLIGHT = 79;

/**
 * Limit of items before show scroll on fields modal
 * @constant
 */
export const limitScrollFieldsModal = 10;

/**
 * The base text for subtitle of Export Dialog (Toolbar)
 * @constant
 */
export const EXPORT_DIALOG_SUBTITLE = "Exportera flöde som JSON-fil.";
/**
 * The base text for subtitle of Flow Settings (Menubar)
 * @constant
 */
export const SETTINGS_DIALOG_SUBTITLE =
  "Anpassa dina flödesdetaljer och inställningar.";

/**
 * The base text for subtitle of Flow Logs (Menubar)
 * @constant
 */
export const LOGS_DIALOG_SUBTITLE =
  "Utforska detaljerade loggar över händelser och transaktioner mellan komponenter.";

/**
 * The base text for subtitle of Code Dialog (Toolbar)
 * @constant
 */
export const CODE_DIALOG_SUBTITLE =
  "Exportera ditt flöde för att integrera det med denna kod.";

/**
 * The base text for subtitle of Chat Form
 * @constant
 */
export const CHAT_FORM_DIALOG_SUBTITLE =
  "Interagera med din AI. Övervaka inmatningar, utmatningar och minnen.";

/**
 * The base text for subtitle of Edit Node Dialog
 * @constant
 */
export const EDIT_DIALOG_SUBTITLE =
  "Justera komponentens inställningar och definiera parametersynlighet. Kom ihåg att spara dina ändringar.";

/**
 * The base text for subtitle of Code Dialog
 * @constant
 */
export const CODE_PROMPT_DIALOG_SUBTITLE =
  "Redigera ditt Python-kodavsnitt. Se Axie Studio-dokumentationen för mer information om hur du skriver din egen komponent.";

export const CODE_DICT_DIALOG_SUBTITLE =
  "Anpassa din ordbok, lägg till eller redigera nyckel-värde-par efter behov. Stöder tillägg av nya objekt {} eller arrayer [].";

/**
 * The base text for subtitle of Prompt Dialog
 * @constant
 */
export const PROMPT_DIALOG_SUBTITLE =
  "Skapa din prompt. Prompter kan hjälpa till att styra beteendet hos en språkmodell. Använd klammerparenteser {} för att introducera variabler.";

export const CHAT_CANNOT_OPEN_TITLE = "Chatten Kan Inte Öppnas";

export const CHAT_CANNOT_OPEN_DESCRIPTION = "Detta är inte ett chattflöde.";

export const FLOW_NOT_BUILT_TITLE = "Flöde inte byggt";

export const FLOW_NOT_BUILT_DESCRIPTION =
  "Vänligen bygg flödet innan du chattar.";

/**
 * The base text for subtitle of Text Dialog
 * @constant
 */
export const TEXT_DIALOG_TITLE = "Redigera textinnehåll";

/**
 * The base text for subtitle of Import Dialog
 * @constant
 */
export const IMPORT_DIALOG_SUBTITLE =
  "Importera flöden från en JSON-fil eller välj från befintliga exempel.";

/**
 * The text that shows when a tooltip is empty
 * @constant
 */
export const TOOLTIP_EMPTY = "Inga kompatibla komponenter hittades.";

export const CSVViewErrorTitle = "CSV-utdata";

export const CSVNoDataError = "Ingen data tillgänglig";

export const PDFViewConstant = "Expandera utdatan för att se PDF:en";

export const CSVError = "Fel vid laddning av CSV";

export const PDFLoadErrorTitle = "Fel vid laddning av PDF";

export const PDFCheckFlow = "Vänligen kontrollera ditt flöde och försök igen";

export const PDFErrorTitle = "PDF-utdata";

export const PDFLoadError = "Kör flödet för att se pdf:en";

export const IMGViewConstant = "Expandera vyn för att se bilden";

export const IMGViewErrorMSG =
  "Kör flödet eller ange en giltig url för att se din bild";

export const IMGViewErrorTitle = "Bildutdata";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const EXPORT_CODE_DIALOG =
  "Generera koden för att integrera ditt flöde i en extern applikation.";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const COLUMN_DIV_STYLE =
  " w-full h-full flex overflow-auto flex-col bg-muted px-16 ";

export const NAV_DISPLAY_STYLE =
  " w-full flex justify-between py-12 pb-2 px-6 ";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const DESCRIPTIONS: string[] = [
  "Kedja Orden, Bemästra Språket!",
  "Språkarkitekt i Arbete!",
  "Stärker Språkingenjörskonst.",
  "Skapa Språkförbindelser Här.",
  "Skapa, Anslut, Konversera.",
  "Smarta Kedjor, Smartare Konversationer.",
  "Bygger Broar mellan Prompter för Briljans.",
  "Språkmodeller, Frisläppta.",
  "Ditt Nav för Textgenerering.",
  "Promptly Genialiskt!",
  "Bygger Språkliga Labyrinter.",
  "Axie Studio: Skapa, Kedja, Kommunicera.",
  "Koppla Prickarna, Skapa Språk.",
  "Interaktiv Språkvävning.",
  "Generera, Innovera, Kommunicera.",
  "Konversationskatalysatormotor.",
  "Språkkedjemästare.",
  "Designa Dialoger med Axie Studio.",
  "Vårda NLP-Noder Här.",
  "Konversationskartografi Upplåst.",
  "Designa, Utveckla, Dialogisera.",
];
export const BUTTON_DIV_STYLE =
  " flex gap-2 focus:ring-1 focus:ring-offset-1 focus:ring-ring focus:outline-none ";

/**
 * The base text for subtitle of code dialog
 * @constant
 */
export const ADJECTIVES: string[] = [
  "admiring",
  "adoring",
  "agitated",
  "amazing",
  "angry",
  "awesome",
  "backstabbing",
  "berserk",
  "big",
  "boring",
  "clever",
  "cocky",
  "compassionate",
  "condescending",
  "cranky",
  "desperate",
  "determined",
  "distracted",
  "dreamy",
  "drunk",
  "ecstatic",
  "elated",
  "elegant",
  "evil",
  "fervent",
  "focused",
  "furious",
  "gigantic",
  "gloomy",
  "goofy",
  "grave",
  "happy",
  "high",
  "hopeful",
  "hungry",
  "insane",
  "jolly",
  "jovial",
  "kickass",
  "lonely",
  "loving",
  "mad",
  "modest",
  "naughty",
  "nauseous",
  "nostalgic",
  "pedantic",
  "pensive",
  "prickly",
  "reverent",
  "romantic",
  "sad",
  "serene",
  "sharp",
  "sick",
  "silly",
  "sleepy",
  "small",
  "stoic",
  "stupefied",
  "suspicious",
  "tender",
  "thirsty",
  "tiny",
  "trusting",
  "bubbly",
  "charming",
  "cheerful",
  "comical",
  "dazzling",
  "delighted",
  "dynamic",
  "effervescent",
  "enthusiastic",
  "exuberant",
  "fluffy",
  "friendly",
  "funky",
  "giddy",
  "giggly",
  "gleeful",
  "goofy",
  "graceful",
  "grinning",
  "hilarious",
  "inquisitive",
  "joyous",
  "jubilant",
  "lively",
  "mirthful",
  "mischievous",
  "optimistic",
  "peppy",
  "perky",
  "playful",
  "quirky",
  "radiant",
  "sassy",
  "silly",
  "spirited",
  "sprightly",
  "twinkly",
  "upbeat",
  "vibrant",
  "witty",
  "zany",
  "zealous",
];
/**
 * Nouns for the name of the flow
 * @constant
 *
 */
export const NOUNS: string[] = [
  "albattani",
  "allen",
  "almeida",
  "archimedes",
  "ardinghelli",
  "aryabhata",
  "austin",
  "babbage",
  "banach",
  "bardeen",
  "bartik",
  "bassi",
  "bell",
  "bhabha",
  "bhaskara",
  "blackwell",
  "bohr",
  "booth",
  "borg",
  "bose",
  "boyd",
  "brahmagupta",
  "brattain",
  "brown",
  "carson",
  "chandrasekhar",
  "colden",
  "cori",
  "cray",
  "curie",
  "darwin",
  "davinci",
  "dijkstra",
  "dubinsky",
  "easley",
  "einstein",
  "elion",
  "engelbart",
  "euclid",
  "euler",
  "fermat",
  "fermi",
  "feynman",
  "franklin",
  "galileo",
  "gates",
  "goldberg",
  "goldstine",
  "goldwasser",
  "golick",
  "goodall",
  "hamilton",
  "hawking",
  "heisenberg",
  "heyrovsky",
  "hodgkin",
  "hoover",
  "hopper",
  "hugle",
  "hypatia",
  "jang",
  "jennings",
  "jepsen",
  "joliot",
  "jones",
  "kalam",
  "kare",
  "keller",
  "khorana",
  "kilby",
  "kirch",
  "knuth",
  "kowalevski",
  "lalande",
  "lamarr",
  "leakey",
  "leavitt",
  "lichterman",
  "liskov",
  "lovelace",
  "lumiere",
  "mahavira",
  "mayer",
  "mccarthy",
  "mcclintock",
  "mclean",
  "mcnulty",
  "meitner",
  "meninsky",
  "mestorf",
  "minsky",
  "mirzakhani",
  "morse",
  "murdock",
  "newton",
  "nobel",
  "noether",
  "northcutt",
  "noyce",
  "panini",
  "pare",
  "pasteur",
  "payne",
  "perlman",
  "pike",
  "poincare",
  "poitras",
  "ptolemy",
  "raman",
  "ramanujan",
  "ride",
  "ritchie",
  "roentgen",
  "rosalind",
  "saha",
  "sammet",
  "shaw",
  "shirley",
  "shockley",
  "sinoussi",
  "snyder",
  "spence",
  "stallman",
  "stonebraker",
  "swanson",
  "swartz",
  "swirles",
  "tesla",
  "thompson",
  "torvalds",
  "turing",
  "varahamihira",
  "visvesvaraya",
  "volhard",
  "wescoff",
  "williams",
  "wilson",
  "wing",
  "wozniak",
  "wright",
  "yalow",
  "yonath",
  "coulomb",
  "degrasse",
  "dewey",
  "edison",
  "eratosthenes",
  "faraday",
  "galton",
  "gauss",
  "herschel",
  "hubble",
  "joule",
  "kaku",
  "kepler",
  "khayyam",
  "lavoisier",
  "maxwell",
  "mendel",
  "mendeleev",
  "ohm",
  "pascal",
  "planck",
  "riemann",
  "schrodinger",
  "sagan",
  "tesla",
  "tyson",
  "volta",
  "watt",
  "weber",
  "wien",
  "zoBell",
  "zuse",
];

/**
 * Header text for user projects
 * @constant
 *
 */
export const USER_PROJECTS_HEADER = "Min Samling";

export const DEFAULT_FOLDER = "Startprojekt";

export const MAX_MCP_SERVER_NAME_LENGTH = 30;

/**
 * Header text for admin page
 * @constant
 *
 */
export const ADMIN_HEADER_TITLE = "Administratörssida";

/**
 * Header description for admin page
 * @constant
 *
 */
export const ADMIN_HEADER_DESCRIPTION =
  "Navigera genom detta avsnitt för att effektivt övervaka alla applikationsanvändare. Härifrån kan du sömlöst hantera användarkonton.";

export const BASE_URL_API = custom.BASE_URL_API || "/api/v1/";

export const BASE_URL_API_V2 = custom.BASE_URL_API_V2 || "/api/v2/";

/**
 * URLs excluded from error retries.
 * @constant
 *
 */
export const URL_EXCLUDED_FROM_ERROR_RETRIES = [
  `${BASE_URL_API}validate/code`,
  `${BASE_URL_API}custom_component`,
  `${BASE_URL_API}validate/prompt`,
  `${BASE_URL_API}/login`,
  `${BASE_URL_API}api_key/store`,
];

export const skipNodeUpdate = [
  "CustomComponent",
  "PromptTemplate",
  "ChatMessagePromptTemplate",
  "SystemMessagePromptTemplate",
  "HumanMessagePromptTemplate",
];

export const CONTROL_INPUT_STATE = {
  password: "",
  cnfPassword: "",
  username: "",
  email: "",
};

export const CONTROL_PATCH_USER_STATE = {
  password: "",
  cnfPassword: "",
  profilePicture: "",
  apikey: "",
};

export const CONTROL_LOGIN_STATE = {
  username: "",
  password: "",
};

export const CONTROL_NEW_USER = {
  username: "",
  email: "",  // Required field for new user creation
  password: "",
  is_active: false,
  is_superuser: false,
};

export const tabsCode = [];

export const FETCH_ERROR_MESSAGE = "Kunde inte upprätta en anslutning.";
export const FETCH_ERROR_DESCRIPION =
  "Kontrollera att allt fungerar korrekt och försök igen.";

export const TIMEOUT_ERROR_MESSAGE =
  "Vänligen vänta några ögonblick medan servern bearbetar din begäran.";
export const TIMEOUT_ERROR_DESCRIPION = "Servern är upptagen.";

export const SIGN_UP_SUCCESS = "Konto skapat! Vänta på administratörsaktivering. ";

export const API_PAGE_PARAGRAPH =
  "Dina hemliga Axie Studio API-nycklar listas nedan. Dela inte din API-nyckel med andra, eller exponera den i webbläsaren eller annan klientkod.";

export const API_PAGE_USER_KEYS =
  "Denna användare har inga nycklar tilldelade för tillfället.";

export const LAST_USED_SPAN_1 = "Senaste gången denna nyckel användes.";

export const LAST_USED_SPAN_2 =
  "Noggrann inom timmen från den senaste användningen.";

export const AXIESTUDIO_SUPPORTED_TYPES = new Set([
  "str",
  "bool",
  "float",
  "code",
  "prompt",
  "file",
  "int",
  "dict",
  "NestedDict",
  "table",
  "link",
  "slider",
  "tab",
  "sortableList",
  "connect",
  "auth",
  "query",
  "mcp",
  "tools",
]);

export const FLEX_VIEW_TYPES = ["bool"];

export const priorityFields = new Set(["code", "template", "mode"]);

export const INPUT_TYPES = new Set([
  "ChatInput",
  // "TextInput",
  // "KeyPairInput",
  // "JsonInput",
  // "StringListInput",
]);
export const OUTPUT_TYPES = new Set([
  "ChatOutput",
  // "TextOutput",
  // "PDFOutput",
  // "ImageOutput",
  // "CSVOutput",
  // "JsonOutput",
  // "KeyPairOutput",
  // "StringListOutput",
  // "DataOutput",
  // "TableOutput",
]);

export const CHAT_FIRST_INITIAL_TEXT =
  "Starta en konversation och klicka på agentens minnen";

export const TOOLTIP_OUTDATED_NODE =
  "Din komponent är föråldrad. Klicka för att uppdatera (data kan gå förlorad)";

export const CHAT_SECOND_INITIAL_TEXT = "för att inspektera tidigare meddelanden.";

export const TOOLTIP_OPEN_HIDDEN_OUTPUTS = "Expandera dolda utdata";
export const TOOLTIP_HIDDEN_OUTPUTS = "Kollapsa dolda utdata";

export const ZERO_NOTIFICATIONS = "Inga nya notifieringar";

export const SUCCESS_BUILD = "Byggd framgångsrikt ✨";

export const ALERT_SAVE_WITH_API =
  "Varning: Att avmarkera denna ruta tar endast bort API-nycklar från fält som specifikt är avsedda för API-nycklar.";

export const SAVE_WITH_API_CHECKBOX = "Spara med mina API-nycklar";
export const EDIT_TEXT_MODAL_TITLE = "Redigera Text";
export const EDIT_TEXT_PLACEHOLDER = "Skriv meddelande här.";
export const INPUT_HANDLER_HOVER = "Tillgängliga inmatningskomponenter:";
export const OUTPUT_HANDLER_HOVER = "Tillgängliga utmatningskomponenter:";
export const TEXT_INPUT_MODAL_TITLE = "Inmatningar";
export const OUTPUTS_MODAL_TITLE = "Utmatningar";
export const AXIESTUDIO_CHAT_TITLE = "Axie Studio Chatt";
export const CHAT_INPUT_PLACEHOLDER =
  "Inga chattinmatningsvariabler hittades. Klicka för att köra ditt flöde.";
export const CHAT_INPUT_PLACEHOLDER_SEND = "Skicka ett meddelande...";
export const EDIT_CODE_TITLE = "Redigera Kod";
export const MY_COLLECTION_DESC =
  "Hantera dina projekt. Ladda ner och ladda upp hela samlingar.";
export const STORE_DESC = "Utforska gemenskapsdelade flöden och komponenter.";
export const STORE_TITLE = "Axie Studio Store";
export const NO_API_KEY = "Du har ingen API-nyckel.";
export const INSERT_API_KEY = "Infoga din Axie Studio API-nyckel.";
export const INVALID_API_KEY = "Din API-nyckel är inte giltig. ";
export const CREATE_API_KEY = `Har du ingen API-nyckel? Registrera dig på`;
export const STATUS_BUILD = "Bygg för att validera status.";
export const STATUS_MISSING_FIELDS_ERROR =
  "Vänligen fyll i alla obligatoriska fält.";
export const STATUS_INACTIVE = "Exekvering blockerad";
export const STATUS_BUILDING = "Bygger...";
export const SAVED_HOVER = "Senast sparad: ";
export const RUN_TIMESTAMP_PREFIX = "Senaste Körning: ";
export const STARTER_FOLDER_NAME = "Startprojekt";
export const PRIORITY_SIDEBAR_ORDER = [
  "saved_components",
  "inputs",
  "outputs",
  "prompts",
  "data",
  "prompt",
  "models",
  "helpers",
  "vectorstores",
  "embeddings",
];

export const BUNDLES_SIDEBAR_FOLDER_NAMES = [
  "notion",
  "Notion",
  "AssemblyAI",
  "assemblyai",
  "LangWatch",
  "langwatch",
  "YouTube",
  "youtube",
];

export const AUTHORIZED_DUPLICATE_REQUESTS = [
  "/health",
  "/flows",
  "/logout",
  "/refresh",
  "/login",
  "/subscriptions/status",
  "/users/whoami",
  "/files",
];

export const BROKEN_EDGES_WARNING =
  "Vissa anslutningar togs bort eftersom de var ogiltiga:";

export const SAVE_DEBOUNCE_TIME = 300;

export const IS_MAC =
  typeof navigator !== "undefined" &&
  navigator.userAgent.toUpperCase().includes("MAC");

export const defaultShortcuts = [
  {
    display_name: "Kontroller",
    name: "Advanced Settings",
    shortcut: "mod+shift+a",
  },
  {
    display_name: "Sök Komponenter i Sidopanel",
    name: "Search Components Sidebar",
    shortcut: "/",
  },
  {
    display_name: "Minimera",
    name: "Minimize",
    shortcut: "mod+.",
  },
  {
    display_name: "Kod",
    name: "Code",
    shortcut: "space",
  },
  {
    display_name: "Kopiera",
    name: "Copy",
    shortcut: "mod+c",
  },
  {
    display_name: "Duplicera",
    name: "Duplicate",
    shortcut: "mod+d",
  },
  {
    display_name: "Komponentdelning",
    name: "Component Share",
    shortcut: "mod+shift+s",
  },
  {
    display_name: "Dokumentation",
    name: "Docs",
    shortcut: "mod+shift+d",
  },
  {
    display_name: "Spara Ändringar",
    name: "Changes Save",
    shortcut: "mod+s",
  },
  {
    display_name: "Spara Komponent",
    name: "Save Component",
    shortcut: "mod+alt+s",
  },
  {
    display_name: "Ta Bort",
    name: "Delete",
    shortcut: "backspace",
  },
  {
    display_name: "Öppna Lekplats",
    name: "Open Playground",
    shortcut: "mod+k",
  },
  {
    display_name: "Ångra",
    name: "Undo",
    shortcut: "mod+z",
  },
  {
    display_name: "Gör Om",
    name: "Redo",
    shortcut: "mod+y",
  },
  {
    display_name: "Gör Om (alternativ)",
    name: "Redo Alt",
    shortcut: "mod+shift+z",
  },
  {
    display_name: "Gruppera",
    name: "Group",
    shortcut: "mod+g",
  },
  {
    display_name: "Klipp Ut",
    name: "Cut",
    shortcut: "mod+x",
  },
  {
    display_name: "Klistra In",
    name: "Paste",
    shortcut: "mod+v",
  },
  {
    display_name: "API",
    name: "API",
    shortcut: "r",
  },
  {
    display_name: "Ladda Ner",
    name: "Download",
    shortcut: "mod+j",
  },
  {
    display_name: "Uppdatera",
    name: "Update",
    shortcut: "mod+u",
  },
  {
    display_name: "Frys",
    name: "Freeze Path",
    shortcut: "mod+shift+f",
  },
  {
    display_name: "Flödesdelning",
    name: "Flow Share",
    shortcut: "mod+shift+b",
  },
  {
    display_name: "Spela",
    name: "Play",
    shortcut: "p",
  },
  {
    display_name: "Utdatainspektion",
    name: "Output Inspection",
    shortcut: "o",
  },
  {
    display_name: "Verktygsläge",
    name: "Tool Mode",
    shortcut: "mod+shift+m",
  },
  {
    display_name: "Växla Sidopanel",
    name: "Toggle Sidebar",
    shortcut: "mod+b",
  },
];

export const DEFAULT_TABLE_ALERT_MSG = `Hoppsan! Det verkar som att det inte finns någon data att visa just nu. Vänligen kom tillbaka senare.`;

export const DEFAULT_TABLE_ALERT_TITLE = "Ingen Data Tillgänglig";

export const NO_COLUMN_DEFINITION_ALERT_TITLE = "Inga Kolumndefinitioner";

export const NO_COLUMN_DEFINITION_ALERT_DESCRIPTION =
  "Det finns inga kolumndefinitioner tillgängliga för denna tabell.";

export const LOCATIONS_TO_RETURN = ["/flow/", "/settings/"];

export const MAX_BATCH_SIZE = 50;

export const MODAL_CLASSES =
  "nopan nodelete nodrag  noflow fixed inset-0 bottom-0 left-0 right-0 top-0 z-50 overflow-auto bg-black/50 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0";

export const ALLOWED_IMAGE_INPUT_EXTENSIONS = ["png", "jpg", "jpeg"];

export const componentsToIgnoreUpdate = ["CustomComponent"];

export const FS_ERROR_TEXT =
  "Vänligen säkerställ att din fil har en av följande filändelser:";
export const SN_ERROR_TEXT = ALLOWED_IMAGE_INPUT_EXTENSIONS.join(", ");

export const ERROR_UPDATING_COMPONENT =
  "Ett oväntat fel uppstod vid uppdatering av komponenten. Vänligen försök igen.";
export const TITLE_ERROR_UPDATING_COMPONENT =
  "Fel vid uppdatering av komponenten";

export const EMPTY_INPUT_SEND_MESSAGE = "Inget inmatningsmeddelande tillhandahållet.";

export const EMPTY_OUTPUT_SEND_MESSAGE = "Meddelandet är tomt.";

export const TABS_ORDER = [
  "curl",
  "python api",
  "js api",
  "python code",
  "chat widget html",
];

export const AXIESTUDIO_ACCESS_TOKEN = "access_token_as";
export const AXIESTUDIO_API_TOKEN = "apikey_tkn_axie";
export const AXIESTUDIO_AUTO_LOGIN_OPTION = "auto_login_as";
export const AXIESTUDIO_REFRESH_TOKEN = "refresh_token_as";

export const AXIESTUDIO_ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 - 60 * 60 * 0.1;
export const AXIESTUDIO_ACCESS_TOKEN_EXPIRE_SECONDS_ENV =
  Number(process.env?.ACCESS_TOKEN_EXPIRE_SECONDS ?? 60) -
  Number(process.env?.ACCESS_TOKEN_EXPIRE_SECONDS ?? 60) * 0.1;
export const TEXT_FIELD_TYPES: string[] = ["str", "SecretStr"];
export const NODE_WIDTH = 384;
export const NODE_HEIGHT = NODE_WIDTH * 3;

export const SHORTCUT_KEYS = ["cmd", "ctrl", "mod", "alt", "shift"];

export const SERVER_HEALTH_INTERVAL = 10000;
export const REFETCH_SERVER_HEALTH_INTERVAL = 20000;
export const DRAG_EVENTS_CUSTOM_TYPESS = {
  genericnode: "genericNode",
  notenode: "noteNode",
  "text/plain": "text/plain",
};

export const NOTE_NODE_MIN_WIDTH = 324;
export const NOTE_NODE_MIN_HEIGHT = 324;
export const NOTE_NODE_MAX_HEIGHT = 800;
export const NOTE_NODE_MAX_WIDTH = 1000;

export const COLOR_OPTIONS = {
  amber: "hsl(var(--note-amber))",
  neutral: "hsl(var(--note-neutral))",
  rose: "hsl(var(--note-rose))",
  blue: "hsl(var(--note-blue))",
  lime: "hsl(var(--note-lime))",
  transparent: null,
};

export const maxSizeFilesInBytes = 10 * 1024 * 1024; // 10MB in bytes
export const MAX_TEXT_LENGTH = 99999;

export const SEARCH_TABS = ["Alla", "Flöden", "Komponenter"];
export const PAGINATION_SIZE = 12;
export const PAGINATION_PAGE = 1;

export const STORE_PAGINATION_SIZE = 12;
export const STORE_PAGINATION_PAGE = 1;

export const PAGINATION_ROWS_COUNT = [12, 24, 48, 96];
export const STORE_PAGINATION_ROWS_COUNT = [12, 24, 48, 96];

export const GRADIENT_CLASS =
  "linear-gradient(to right, hsl(var(--background) / 0.3), hsl(var(--background)))";

export const GRADIENT_CLASS_DISABLED =
  "linear-gradient(to right, hsl(var(--muted) / 0.3), hsl(var(--muted)))";

export const RECEIVING_INPUT_VALUE = "Tar emot inmatning";
export const SELECT_AN_OPTION = "Välj ett alternativ";

export const ICON_STROKE_WIDTH = 1.5;

export const DEFAULT_PLACEHOLDER = "Skriv något...";

export const DEFAULT_TOOLSET_PLACEHOLDER = "Används som verktyg";

export const SAVE_API_KEY_ALERT = "API-nyckel sparad framgångsrikt";
export const PLAYGROUND_BUTTON_NAME = "Lekplats";
export const POLLING_MESSAGES = {
  ENDPOINT_NOT_AVAILABLE: "Slutpunkt inte tillgänglig",
  STREAMING_NOT_SUPPORTED: "Streaming stöds inte",
} as const;

export const BUILD_POLLING_INTERVAL = 25;

export const IS_AUTO_LOGIN = false;

export const AUTO_LOGIN_RETRY_DELAY = 2000;
export const AUTO_LOGIN_MAX_RETRY_DELAY = 60000;

export const ALL_LANGUAGES = [
  { value: "en-US", name: "Engelska (USA)" },
  { value: "en-GB", name: "Engelska (Storbritannien)" },
  { value: "it-IT", name: "Italienska" },
  { value: "fr-FR", name: "Franska" },
  { value: "es-ES", name: "Spanska" },
  { value: "de-DE", name: "Tyska" },
  { value: "ja-JP", name: "Japanska" },
  { value: "pt-BR", name: "Portugisiska (Brasilien)" },
  { value: "zh-CN", name: "Kinesiska (Förenklad)" },
  { value: "ru-RU", name: "Ryska" },
  { value: "ar-SA", name: "Arabiska" },
  { value: "hi-IN", name: "Hindi" },
];

export const DEBOUNCE_FIELD_LIST = [
  "SecretStrInput",
  "MessageTextInput",
  "TextInput",
  "MultilineInput",
  "SecretStrInput",
  "IntInput",
  "FloatInput",
  "SliderInput",
];

export const OPENAI_VOICES = [
  { name: "alloy", value: "alloy" },
  { name: "ash", value: "ash" },
  { name: "ballad", value: "ballad" },
  { name: "coral", value: "coral" },
  { name: "echo", value: "echo" },
  { name: "sage", value: "sage" },
  { name: "shimmer", value: "shimmer" },
  { name: "verse", value: "verse" },
];

export const DEFAULT_POLLING_INTERVAL = 5000;
export const DEFAULT_TIMEOUT = 30000;
export const DEFAULT_FILE_PICKER_TIMEOUT = 60000;
export const DISCORD_URL = "";
export const GITHUB_URL = "";
export const TWITTER_URL = "";
export const DOCS_URL = "https://docs.axiestudio.se";
export const DATASTAX_DOCS_URL = "";

export const UUID_PARSING_ERROR = "uuid_parsing";
