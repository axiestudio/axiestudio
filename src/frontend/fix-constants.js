const fs = require('fs');

// Fix flow_constants.tsx by removing all t() calls
let content = fs.readFileSync('src/flow_constants.tsx', 'utf8');

// Replace all t("...") calls with simple English strings
const replacements = [
  { regex: /t\("common\.promptlyingenious"\)/g, replacement: '"Promptly ingenious"' },
  { regex: /t\("common\.buildinglinguisticlabyrinths"\)/g, replacement: '"Building linguistic labyrinths"' },
  { regex: /t\("actions\.createchaincommunicate"\)/g, replacement: '"Create, chain, communicate"' },
  { regex: /t\("common\.connectthedotscraft"\)/g, replacement: '"Connect the dots, craft"' },
  { regex: /t\("common\.interactivelanguageweaving"\)/g, replacement: '"Interactive language weaving"' },
  { regex: /t\("common\.generateinnovatecommunicate"\)/g, replacement: '"Generate, innovate, communicate"' },
  { regex: /t\("chat\.conversationcatalystengine"\)/g, replacement: '"Conversation catalyst engine"' },
  { regex: /t\("common\.languagechainlinkmaster"\)/g, replacement: '"Language chain link master"' },
  { regex: /t\("common\.designdialogueswithaxie"\)/g, replacement: '"Design dialogues with Axie"' },
  { regex: /t\("flows\.nurturenlpnodeshere"\)/g, replacement: '"Nurture NLP nodes here"' },
  { regex: /t\("chat\.conversationalcartographyunloc"\)/g, replacement: '"Conversational cartography unlocked"' },
  { regex: /t\("common\.designdevelopdialogize"\)/g, replacement: '"Design, develop, dialogize"' },
  { regex: /t\("greetings\.unleashinglinguisticcreativity"\)/g, replacement: '"Unleashing linguistic creativity"' },
  { regex: /t\("chat\.graphyourwayto"\)/g, replacement: '"Graph your way to"' },
  { regex: /t\("common\.thepoweroflanguage"\)/g, replacement: '"The power of language"' },
  { regex: /t\("common\.sculptinglanguagewithprecision"\)/g, replacement: '"Sculpting language with precision"' },
  { regex: /t\("common\.wherelanguagemeetslogic"\)/g, replacement: '"Where language meets logic"' },
  { regex: /t\("common\.buildingintelligentinteraction"\)/g, replacement: '"Building intelligent interaction"' },
  { regex: /t\("common\.yourpassporttolinguistic"\)/g, replacement: '"Your passport to linguistic"' },
  { regex: /t\("actions\.createcuratecommunicatewith"\)/g, replacement: '"Create, curate, communicate with"' },
  { regex: /t\("flows\.flowintothefuture"\)/g, replacement: '"Flow into the future"' },
  { regex: /t\("chat\.mappingmeaningfulconversations"\)/g, replacement: '"Mapping meaningful conversations"' },
  { regex: /t\("common\.unraveltheartof"\)/g, replacement: '"Unravel the art of"' },
  { regex: /t\("common\.languageengineeringexcellence"\)/g, replacement: '"Language engineering excellence"' },
  { regex: /t\("chat\.navigatethenetworksof"\)/g, replacement: '"Navigate the networks of"' },
  { regex: /t\("flows\.craftingconversationsonenode"\)/g, replacement: '"Crafting conversations one node"' },
  { regex: /t\("common\.thepinnacleofprompt"\)/g, replacement: '"The pinnacle of prompt"' },
  { regex: /t\("common\.languagemodelsmappedand"\)/g, replacement: '"Language models mapped and"' },
  { regex: /t\("common\.powerfulpromptsperfectlypositi"\)/g, replacement: '"Powerful prompts perfectly positioned"' },
  { regex: /t\("common\.innovationininteractionwith"\)/g, replacement: '"Innovation in interaction with"' },
  { regex: /t\("common\.yourtoolkitfortext"\)/g, replacement: '"Your toolkit for text"' },
  { regex: /t\("common\.unfoldinglinguisticpossibiliti"\)/g, replacement: '"Unfolding linguistic possibilities"' },
  { regex: /t\("common\.buildingpowerfulsolutionswith"\)/g, replacement: '"Building powerful solutions with"' },
  { regex: /t\("common\.uncoverbusinessopportunitieswi"\)/g, replacement: '"Uncover business opportunities with"' },
  { regex: /t\("chat\.harnessthepowerof"\)/g, replacement: '"Harness the power of"' },
  { regex: /t\("common\.transformyourbusinesswith"\)/g, replacement: '"Transform your business with"' },
  { regex: /t\("common\.craftmeaningfulinteractionsgen"\)/g, replacement: '"Craft meaningful interactions"' },
  { regex: /t\("greetings\.unleashingbusinesspotentialthr"\)/g, replacement: '"Unleashing business potential through"' },
  { regex: /t\("common\.empoweringenterpriseswithintel"\)/g, replacement: '"Empowering enterprises with intelligence"' },
  { regex: /t\("common\.drivinginnovationinbusiness"\)/g, replacement: '"Driving innovation in business"' },
  { regex: /t\("chat\.catalyzingbusinessgrowththroug"\)/g, replacement: '"Catalyzing business growth through"' },
  { regex: /t\("common\.textgenerationmeetsbusiness"\)/g, replacement: '"Text generation meets business"' },
  { regex: /t\("common\.navigatethelinguisticlandscape"\)/g, replacement: '"Navigate the linguistic landscape"' },
  { regex: /t\("actions\.createpowerfulconnectionsboost"\)/g, replacement: '"Create powerful connections, boost"' },
  { regex: /t\("common\.empoweringcommunicationenablin"\)/g, replacement: '"Empowering communication, enabling"' },
  { regex: /t\("common\.advancednlpforgroundbreaking"\)/g, replacement: '"Advanced NLP for groundbreaking"' },
  { regex: /t\("common\.innovationininteractionrevolut"\)/g, replacement: '"Innovation in interaction, revolution"' },
  { regex: /t\("chat\.maximizeimpactwithintelligent"\)/g, replacement: '"Maximize impact with intelligent"' },
  { regex: /t\("greetings\.beyondtextgenerationunleashing"\)/g, replacement: '"Beyond text generation, unleashing"' },
  { regex: /t\("chat\.unlockthepowerof"\)/g, replacement: '"Unlock the power of"' },
  { regex: /t\("common\.craftingdialoguesthatdrive"\)/g, replacement: '"Crafting dialogues that drive"' },
];

// Apply all replacements
replacements.forEach(({ regex, replacement }) => {
  content = content.replace(regex, replacement);
});

// Also replace any remaining t("...") patterns with generic strings
content = content.replace(/t\("([^"]+)"\)/g, (match, key) => {
  // Convert key to readable string
  const readable = key.split('.').pop().replace(/([A-Z])/g, ' $1').toLowerCase();
  return `"${readable.charAt(0).toUpperCase() + readable.slice(1)}"`;
});

fs.writeFileSync('src/flow_constants.tsx', content);
console.log('✅ Fixed flow_constants.tsx');

// Fix other files with t() calls in constants
const filesToFix = [
  'src/types/factory/axios-error-503.ts',
];

filesToFix.forEach(file => {
  try {
    let fileContent = fs.readFileSync(file, 'utf8');
    
    // Remove useTranslation import
    fileContent = fileContent.replace(/import.*useTranslation.*from.*react-i18next.*;\s*/g, '');
    
    // Replace t() calls with simple strings
    fileContent = fileContent.replace(/t\("common\.serviceunavailable"\)/g, '"Service Unavailable"');
    fileContent = fileContent.replace(/t\("common\.serveriscurrentlybusy"\)/g, '"Server is currently busy"');
    
    fs.writeFileSync(file, fileContent);
    console.log(`✅ Fixed ${file}`);
  } catch (error) {
    console.log(`⚠️ Could not fix ${file}: ${error.message}`);
  }
});

console.log('🎉 Fixed all constant files!');
