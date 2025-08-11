const fs = require('fs');
const path = require('path');

/**
 * Comprehensive string replacement script for Axiestudio Swedish translation
 * This script finds and replaces hardcoded English strings with translation calls
 */

// Common string mappings for automatic translation
const STRING_MAPPINGS = {
  // Navigation and UI
  '"My Collection"': 't("navigation.myCollection")',
  '"Axie Studio Store"': 't("navigation.store")',
  '"Admin Page"': 't("navigation.adminPage")',
  '"Playground"': 't("navigation.playground")',
  '"My Files"': 't("navigation.myFiles")',
  
  // Common actions
  '"Save"': 't("common.save")',
  '"Cancel"': 't("common.cancel")',
  '"Delete"': 't("common.delete")',
  '"Edit"': 't("common.edit")',
  '"Add"': 't("common.add")',
  '"Close"': 't("common.close")',
  '"Confirm"': 't("common.confirm")',
  '"Yes"': 't("common.yes")',
  '"No"': 't("common.no")',
  '"Build"': 't("common.build")',
  '"Run"': 't("common.run")',
  '"Stop"': 't("common.stop")',
  '"Copy"': 't("common.copy")',
  '"Search"': 't("common.search")',
  '"Filter"': 't("common.filter")',
  '"Settings"': 't("common.settings")',
  '"Help"': 't("common.help")',
  '"Loading..."': 't("common.loading")',
  
  // Sidebar components
  '"Saved"': 't("sidebar.savedComponents")',
  '"Input / Output"': 't("sidebar.inputOutput")',
  '"Agents"': 't("sidebar.agents")',
  '"Models"': 't("sidebar.models")',
  '"Data"': 't("sidebar.data")',
  '"Vector Stores"': 't("sidebar.vectorStores")',
  '"Processing"': 't("sidebar.processing")',
  '"Logic"': 't("sidebar.logic")',
  '"Helpers"': 't("sidebar.helpers")',
  '"Inputs"': 't("sidebar.inputs")',
  '"Outputs"': 't("sidebar.outputs")',
  
  // Flow status messages
  '"Build to validate status."': 't("flows.buildToValidate")',
  '"Please fill all the required fields."': 't("flows.fillRequiredFields")',
  '"Execution blocked"': 't("flows.executionBlocked")',
  '"Building..."': 't("flows.building")',
  '"Built successfully ✨"': 't("flows.builtSuccessfully")',
  
  // File management
  '"Please select a valid file. Only these file types are allowed:"': 't("fileManagement.selectValidFile")',
  '"Error occurred while uploading file"': 't("fileManagement.fileUploadError")',
  
  // Components
  '"Your component is outdated. Click to update (data may be lost)"': 't("components.outdatedComponent")',
  '"Expand hidden outputs"': 't("components.expandHiddenOutputs")',
  '"Collapse hidden outputs"': 't("components.collapseHiddenOutputs")',
  '"Available input components:"': 't("components.availableInputComponents")',
  '"Available output components:"': 't("components.availableOutputComponents")',
  
  // Messages
  '"No input message provided."': 't("messages.noInputMessage")',
  '"Message empty."': 't("messages.emptyMessage")',
  '"Send a message..."': 't("messages.sendMessage")',
  '"Type message here."': 't("messages.typeMessage")',
  
  // Placeholders
  '"Type something..."': 't("common.defaultPlaceholder")',
  '"Select an option"': 't("common.selectAnOption")',
  '"Used as a tool"': 't("common.defaultToolsetPlaceholder")',
  '"Receiving input"': 't("common.receivingInputValue")',
  
  // Auth
  '"Welcome to Axie Studio"': 't("auth.welcome")',
  '"Sign in to continue to your workspace"': 't("auth.signInSubtitle")',
  '"Username"': 't("auth.username")',
  '"Password"': 't("auth.password")',
  '"Sign in"': 't("auth.signIn")',
  '"Enter your username"': 't("auth.enterUsername")',
  '"Enter your password"': 't("auth.enterPassword")',
  
  // Projects
  '"Manage your projects. Download and upload entire collections."': 't("projects.myCollectionDesc")',
  '"Explore community-shared flows and components."': 't("projects.storeDesc")',
  '"Starter Project"': 't("projects.defaultFolder")',
  
  // API
  '"Your secret Axie Studio API keys are listed below. Do not share your API key with others, or expose it in the browser or other client-side code."': 't("api.apiPageParagraph")',
  '"This user does not have any keys assigned at the moment."': 't("api.apiPageUserKeys")',
  '"You don\'t have an API key."': 't("api.noApiKey")',
  '"Insert your Axie Studio API key."': 't("api.insertApiKey")',
  '"Your API key is not valid."': 't("api.invalidApiKey")',
  '"API key saved successfully"': 't("api.saveApiKeyAlert")',
  
  // Chat
  '"Axie Studio Chat"': 't("chat.axiestudioChatTitle")',
  '"No chat input variables found. Click to run your flow."': 't("chat.chatInputPlaceholder")',
  '"Start a conversation and click the agent\'s memories"': 't("chat.chatFirstInitialText")',
  '"to inspect previous messages."': 't("chat.chatSecondInitialText")',
  
  // Notifications
  '"No new notifications"': 't("notifications.zeroNotifications")'
};

// Files to process (add more as needed)
const TARGET_DIRECTORIES = [
  'src/components',
  'src/pages',
  'src/modals',
  'src/customization'
];

// File extensions to process
const FILE_EXTENSIONS = ['.tsx', '.ts', '.jsx', '.js'];

function shouldProcessFile(filePath) {
  const ext = path.extname(filePath);
  return FILE_EXTENSIONS.includes(ext) && 
         !filePath.includes('node_modules') &&
         !filePath.includes('build') &&
         !filePath.includes('dist') &&
         !filePath.includes('i18n') &&
         !filePath.includes('localized');
}

function addTranslationImport(content) {
  // Check if useTranslation is already imported
  if (content.includes('useTranslation')) {
    return content;
  }
  
  // Find React imports and add useTranslation
  const reactImportRegex = /import\s+.*from\s+['"]react['"];?/;
  const i18nImport = `import { useTranslation } from 'react-i18next';`;
  
  if (reactImportRegex.test(content)) {
    return content.replace(reactImportRegex, (match) => `${match}\n${i18nImport}`);
  }
  
  // If no React import, add at the top
  return `${i18nImport}\n${content}`;
}

function addTranslationHook(content) {
  // Check if t hook is already declared
  if (content.includes('const { t }') || content.includes('const {t}')) {
    return content;
  }
  
  // Find function component declarations and add translation hook
  const functionRegex = /(export\s+(?:default\s+)?(?:const|function)\s+\w+.*?\{)/;
  const hookDeclaration = `  const { t } = useTranslation();\n`;
  
  return content.replace(functionRegex, (match) => `${match}\n${hookDeclaration}`);
}

function replaceStrings(content) {
  let updatedContent = content;
  
  for (const [original, replacement] of Object.entries(STRING_MAPPINGS)) {
    // Replace exact string matches
    updatedContent = updatedContent.replace(new RegExp(original.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), replacement);
  }
  
  return updatedContent;
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    // Apply transformations
    content = replaceStrings(content);
    
    // Only add imports and hooks if we made string replacements
    if (content !== originalContent) {
      content = addTranslationImport(content);
      content = addTranslationHook(content);
      
      // Write back to file
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Processed: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return false;
  }
}

function processDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    console.log(`⚠️  Directory not found: ${dirPath}`);
    return;
  }
  
  const items = fs.readdirSync(dirPath);
  
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      processDirectory(fullPath);
    } else if (shouldProcessFile(fullPath)) {
      processFile(fullPath);
    }
  }
}

function main() {
  console.log('🌍 Starting Axiestudio Swedish Translation...\n');
  
  let processedFiles = 0;
  
  for (const dir of TARGET_DIRECTORIES) {
    console.log(`📁 Processing directory: ${dir}`);
    processDirectory(dir);
  }
  
  console.log(`\n🎉 Translation complete! Processed files with string replacements.`);
  console.log('📝 Next steps:');
  console.log('   1. Review the changes');
  console.log('   2. Test the application');
  console.log('   3. Build and deploy');
}

if (require.main === module) {
  main();
}

module.exports = { processFile, processDirectory, STRING_MAPPINGS };
