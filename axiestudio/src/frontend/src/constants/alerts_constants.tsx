// ERROR
export const MISSED_ERROR_ALERT = "Hoppsan! Det verkar som att du missade något";
export const INCOMPLETE_LOOP_ERROR_ALERT =
  "Flödet har en ofullständig loop. Kontrollera dina anslutningar och försök igen.";
export const INVALID_FILE_ALERT =
  "Vänligen välj en giltig fil. Endast dessa filtyper är tillåtna:";
export const CONSOLE_ERROR_MSG = "Ett fel uppstod vid filuppladdning";
export const CONSOLE_SUCCESS_MSG = "Filen laddades upp framgångsrikt";
export const INFO_MISSING_ALERT =
  "Hoppsan! Det verkar som att du missade viss obligatorisk information:";
export const FUNC_ERROR_ALERT = "Det finns ett fel i din funktion";
export const IMPORT_ERROR_ALERT = "Det finns ett fel i dina importer";
export const BUG_ALERT = "Något gick fel, vänligen försök igen";
export const CODE_ERROR_ALERT =
  "Det är något fel med denna kod, vänligen granska den";
export const CHAT_ERROR_ALERT =
  "Vänligen bygg flödet igen innan du använder chatten.";
export const MSG_ERROR_ALERT = "Det uppstod ett fel vid sändning av meddelandet";
export const PROMPT_ERROR_ALERT =
  "Det är något fel med denna prompt, vänligen granska den";
export const API_ERROR_ALERT =
  "Det uppstod ett fel vid sparande av API-nyckeln, vänligen försök igen.";
export const USER_DEL_ERROR_ALERT = "Fel vid borttagning av användare";
export const USER_EDIT_ERROR_ALERT = "Fel vid redigering av användare";
export const USER_ADD_ERROR_ALERT = "Fel vid tillägg av ny användare";
export const SIGNIN_ERROR_ALERT = "Fel vid inloggning";
export const DEL_KEY_ERROR_ALERT = "Fel vid borttagning av nyckel";
export const DEL_KEY_ERROR_ALERT_PLURAL = "Fel vid borttagning av nycklar";
export const UPLOAD_ERROR_ALERT = "Fel vid filuppladdning";
export const WRONG_FILE_ERROR_ALERT = "Ogiltig filtyp";
export const UPLOAD_ALERT_LIST = "Vänligen ladda upp en JSON-fil";
export const INVALID_SELECTION_ERROR_ALERT = "Ogiltigt val";
export const EDIT_PASSWORD_ERROR_ALERT = "Fel vid ändring av lösenord";
export const EDIT_PASSWORD_ALERT_LIST = "Lösenorden stämmer inte överens";
export const SAVE_ERROR_ALERT = "Fel vid sparande av ändringar";
export const PROFILE_PICTURES_GET_ERROR_ALERT =
  "Fel vid hämtning av profilbilder";
export const SIGNUP_ERROR_ALERT = "Fel vid registrering";
export const APIKEY_ERROR_ALERT = "API-nyckelfel";
export const NOAPI_ERROR_ALERT =
  "Du har ingen API-nyckel. Vänligen lägg till en för att använda Axie Studio Store.";
export const INVALID_API_ERROR_ALERT =
  "Din API-nyckel är inte giltig. Vänligen lägg till en giltig API-nyckel för att använda Axie Studio Store.";
export const COMPONENTS_ERROR_ALERT = "Fel vid hämtning av komponenter.";

// NOTICE
export const NOCHATOUTPUT_NOTICE_ALERT =
  "Det finns ingen ChatOutput-komponent i flödet.";
export const API_WARNING_NOTICE_ALERT =
  "Varning: Kritisk data, JSON-filen kan innehålla API-nycklar.";
export const COPIED_NOTICE_ALERT = "API-nyckel kopierad!";
export const TEMP_NOTICE_ALERT = "Din mall har inga variabler.";

// SUCCESS
export const CODE_SUCCESS_ALERT = "Koden är redo att köras";
export const PROMPT_SUCCESS_ALERT = "Prompten är redo";
export const API_SUCCESS_ALERT = "Framgång! Din API-nyckel har sparats.";
export const USER_DEL_SUCCESS_ALERT = "Framgång! Användare borttagen!";
export const USER_EDIT_SUCCESS_ALERT = "Framgång! Användare redigerad!";
export const USER_ADD_SUCCESS_ALERT = "Framgång! Ny användare tillagd!";
export const DEL_KEY_SUCCESS_ALERT = "Framgång! Nyckel borttagen!";
export const DEL_KEY_SUCCESS_ALERT_PLURAL = "Framgång! Nycklar borttagna!";
export const FLOW_BUILD_SUCCESS_ALERT = `Flödet byggdes framgångsrikt`;
export const SAVE_SUCCESS_ALERT = "Ändringar sparade framgångsrikt!";
export const INVALID_FILE_SIZE_ALERT = (maxSizeMB) => {
  return `Filstorleken är för stor. Vänligen välj en fil mindre än ${maxSizeMB}.`;
};
