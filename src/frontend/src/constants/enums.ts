import { useTranslation } from "react-i18next";
/**
 * enum for the different types of nodes
 * @enum
 */
export enum TypeModal {
  TEXT = 1,
  PROMPT = 2,
}

export enum BuildStatus {
  BUILDING = "BUILDING",
  TO_BUILD = "TO_BUILD",
  BUILT = "BUILT",
  INACTIVE = "INACTIVE",
  ERROR = "ERROR",
}

export enum InputOutput {
  INPUT = "input",
  OUTPUT = "output",
}

export enum IOInputTypes {
  TEXT = "Text Input",
  FILE_LOADER = "File Loader",
  KEYPAIR = "Key Pair Input",
  JSON = "JSON Input",
  STRING_LIST = "String List Input",
}

export enum IOOutputTypes {
  TEXT = "Text Output",
  PDF = "PDF Output",
  CSV = "CSV Output",
  IMAGE = "Image Output",
  JSON = "JSON Output",
  KEY_PAIR = "Key Pair Output",
  STRING_LIST = "String List Output",
  DATA = "Data Output",
}

export enum EventDeliveryType {
  STREAMING = "streaming",
  POLLING = "polling",
  DIRECT = "direct",
}
