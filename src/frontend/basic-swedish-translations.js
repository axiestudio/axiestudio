const fs = require('fs');

// Basic Swedish translations for the most important UI strings
const swedishTranslations = {
  "actions": {
    "addnew": "Lägg till ny",
    "addnewvariable": "Lägg till ny variabel",
    "createapikey": "Skapa API-nyckel",
    "createasecretapi": "Skapa hemlig API",
    "createchaincommunicate": "Skapa kedja kommunicera",
    "createconnectconverse": "Skapa anslut konversera",
    "createcuratecommunicatewith": "Skapa kurera kommunicera med",
    "created": "Skapad",
    "createpowerfulconnectionsboost": "Skapa kraftfulla anslutningar boost",
    "createyourfirstflow": "Skapa ditt första flöde",
    "delete": "Radera",
    "editdetails": "Redigera detaljer",
    "flowcreatedsuccessfully": "Flöde skapat framgångsrikt",
    "newcomponentsuccessfullysaved": "Ny komponent framgångsrikt sparad",
    "save": "Spara",
    "savedsuccessfully": "Sparat framgångsrikt",
    "saveApiKeyAlert": "Spara API-nyckel varning"
  },
  "auth": {
    "oauth": "OAuth",
    "password": "Lösenord",
    "username": "Användarnamn",
    "welcome": "Välkommen"
  },
  "chat": {
    "catalyzingbusinessgrowththroug": "Katalyserar affärstillväxt genom",
    "conversationalcartographyunloc": "Konversationskartografi låser upp",
    "conversationcatalystengine": "Konversationskatalysatormotor",
    "graphyourwayto": "Kartlägg din väg till",
    "harnessthepowerof": "Utnyttja kraften av",
    "mappingmeaningfulconversations": "Kartlägga meningsfulla konversationer",
    "maximizeimpactwithintelligent": "Maximera påverkan med intelligent",
    "navigatethenetworksof": "Navigera nätverken av",
    "smartchainssmarterconversation": "Smarta kedjor smartare konversation",
    "unlockthepowerof": "Lås upp kraften av"
  },
  "common": {
    "advancednlpforgroundbreaking": "Avancerad NLP för banbrytande",
    "apikey": "API-nyckel",
    "applytofields": "Tillämpa på fält",
    "axiestudio": "Axiestudio",
    "axiestudioapikeys": "Axiestudio API-nycklar",
    "basic": "Grundläggande",
    "bearertoken": "Bearer-token",
    "beta": "Beta",
    "bundles": "Paket",
    "cancel": "Avbryt",
    "clearyoursearch": "Rensa din sökning",
    "close": "Stäng",
    "confirm": "Bekräfta",
    "copy": "Kopiera",
    "csvoutput": "CSV-utdata",
    "ctrl": "Ctrl",
    "dataoutput": "Datautdata",
    "defaultPlaceholder": "Standard platshållare",
    "delete": "Radera",
    "edit": "Redigera",
    "ensureallrequiredfields": "Säkerställ alla obligatoriska fält",
    "expandtheviewto": "Expandera vyn till",
    "export": "Exportera",
    "filter": "Filter",
    "generateapikey": "Generera API-nyckel",
    "globalvariables": "Globala variabler",
    "gotoserver": "Gå till server",
    "imageoutput": "Bildutdata",
    "jsoninput": "JSON-indata",
    "jsonoutput": "JSON-utdata",
    "keypairinput": "Nyckelpar-indata",
    "keypairoutput": "Nyckelpar-utdata",
    "lastused": "Senast använd",
    "legacy": "Äldre",
    "loading": "Laddar",
    "logs": "Loggar",
    "looping": "Looping",
    "manageglobalvariablesand": "Hantera globala variabler och",
    "missingrequiredfields": "Saknade obligatoriska fält",
    "myapikey": "Min API-nyckel",
    "none": "Ingen",
    "outputs": "Utdata",
    "pdfoutput": "PDF-utdata",
    "preferredlanguage": "Föredraget språk",
    "save": "Spara",
    "search": "Sök",
    "selectAnOption": "Välj ett alternativ",
    "selectedfieldswillautoapply": "Valda fält kommer automatiskt att tillämpas",
    "serveriscurrentlybusy": "Servern är för närvarande upptagen",
    "serviceunavailable": "Tjänsten är inte tillgänglig",
    "settings": "Inställningar",
    "show": "Visa",
    "stepstofix": "Steg för att fixa",
    "stringlistinput": "Stränglista-indata",
    "stringlistoutput": "Stränglista-utdata",
    "textinput": "Textindata",
    "textoutput": "Textutdata",
    "totaluses": "Totala användningar",
    "type": "Typ",
    "value": "Värde"
  },
  "descriptions": {
    "oopslookslikeyou": "Hoppsan, det verkar som om du"
  },
  "errors": {
    "errordetails": "Feldetaljer",
    "errordownloadingfiles": "Fel vid nedladdning av filer"
  },
  "fileManagement": {
    "fileUploadError": "Filuppladdningsfel"
  },
  "files": {
    "fileloader": "Filladdare",
    "pleaseselectavalid": "Vänligen välj en giltig"
  },
  "flows": {
    "checkthecomponentsettings": "Kontrollera komponentinställningarna",
    "craftingconversationsonenode": "Skapa konversationer en nod",
    "flowintothefuture": "Flöda in i framtiden",
    "nocomponentsfound": "Inga komponenter hittades",
    "nurturenlpnodeshere": "Vårda NLP-noder här",
    "rerunyourflow": "Kör ditt flöde igen",
    "theflowhasan": "Flödet har en"
  },
  "greetings": {
    "beyondtextgenerationunleashing": "Bortom textgenerering frigör",
    "languagearchitectatwork": "Språkarkitekt på jobbet",
    "thiscantbeundone": "Detta kan inte ångras",
    "thisoutputhasbeen": "Denna utdata har varit",
    "unleashingbusinesspotentialthr": "Frigöra affärspotential genom",
    "unleashinglinguisticcreativity": "Frigöra språklig kreativitet"
  },
  "labels": {
    "name": "Namn",
    "variablename": "Variabelnamn"
  },
  "messages": {
    "sendMessage": "Skicka meddelande"
  },
  "navigation": {
    "playground": "Lekplats",
    "store": "Butik"
  },
  "settings": {
    "managesettingsrelatedto": "Hantera inställningar relaterade till"
  },
  "sidebar": {
    "agents": "Agenter"
  }
};

// Function to merge translations with existing structure
function mergeTranslations() {
  try {
    console.log('🇸🇪 Applying basic Swedish translations...');
    
    // Read existing English translations
    const enPath = '../backend/translations/en.json';
    const svPath = '../backend/translations/sv.json';
    
    if (!fs.existsSync(enPath)) {
      throw new Error(`English translation file not found: ${enPath}`);
    }
    
    const englishTranslations = JSON.parse(fs.readFileSync(enPath, 'utf8'));
    console.log(`📖 Loaded English translations from: ${enPath}`);
    
    // Read existing Swedish translations
    let existingSwedish = {};
    if (fs.existsSync(svPath)) {
      existingSwedish = JSON.parse(fs.readFileSync(svPath, 'utf8'));
      console.log(`📖 Loaded existing Swedish translations from: ${svPath}`);
    }
    
    // Create Swedish translations by merging our translations with English structure
    const mergedSwedish = createSwedishTranslations(englishTranslations, swedishTranslations);

    // Save updated Swedish translations
    fs.writeFileSync(svPath, JSON.stringify(mergedSwedish, null, 2));
    console.log(`✅ Swedish translations saved to: ${svPath}`);

    // Count translated vs untranslated
    const stats = countTranslations(mergedSwedish, englishTranslations);
    console.log(`📊 Translation Statistics:`);
    console.log(`   ✅ Translated: ${stats.translated} keys`);
    console.log(`   ⏳ Remaining: ${stats.remaining} keys`);
    console.log(`   📈 Progress: ${Math.round((stats.translated / (stats.translated + stats.remaining)) * 100)}%`);
    
    console.log('🎉 Basic Swedish translation complete!');
    
  } catch (error) {
    console.error('❌ Translation failed:', error.message);
    process.exit(1);
  }
}

// Create Swedish translations function
function createSwedishTranslations(english, swedish) {
  const result = {};

  for (const [key, value] of Object.entries(english)) {
    if (typeof value === 'object' && value !== null) {
      // Recursively handle nested objects
      result[key] = createSwedishTranslations(value, swedish[key] || {});
    } else {
      // Use Swedish translation if available, otherwise use English
      result[key] = swedish[key] || value;
    }
  }

  return result;
}

// Count translation statistics
function countTranslations(swedish, english) {
  let translated = 0;
  let remaining = 0;
  
  function countRecursive(sv, en) {
    for (const [key, value] of Object.entries(en)) {
      if (typeof value === 'object' && value !== null) {
        countRecursive(sv[key] || {}, value);
      } else {
        if (sv[key] && sv[key] !== value) {
          translated++;
        } else {
          remaining++;
        }
      }
    }
  }
  
  countRecursive(swedish, english);
  return { translated, remaining };
}

// Run the translation
mergeTranslations();
