#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// List of files that need fixing
const filesToFix = [
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellEditor/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/TableOptions/index.tsx',
  'src/CustomNodes/GenericNode/components/outputModal/index.tsx',
  'src/CustomNodes/NoteNode/components/select-items.tsx',
  'src/modals/deleteConfirmationModal/index.tsx',
  'src/modals/IOModal/components/chatView/chatInput/components/text-area-wrapper.tsx',
  'src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/language-select.tsx',
  'src/modals/templatesModal/index.tsx',
  'src/pages/FlowPage/components/flowSidebarComponent/components/emptySearchComponent/index.tsx',
  'src/pages/FlowPage/components/flowSidebarComponent/components/featureTogglesComponent/index.tsx',
  'src/pages/FlowPage/components/flowSidebarComponent/components/searchInput/index.tsx',
  'src/pages/SettingsPage/pages/ApiKeysPage/components/ApiKeyHeader/index.tsx',
  'src/pages/SettingsPage/pages/GeneralPage/components/PasswordForm/index.tsx',
  'src/shared/components/textOutputView/index.tsx'
];

function addMissingHook(filePath) {
  try {
    const fullPath = path.join(__dirname, filePath);
    let content = fs.readFileSync(fullPath, 'utf8');
    let modified = false;

    console.log(`Checking: ${filePath}`);

    // Check if it has translation calls
    const hasTranslationCalls = /\bt\s*\(\s*["'`]/.test(content);
    
    // Check if it has useTranslation import
    const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
    
    // Check if it has the hook call
    const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)/.test(content);

    if (hasTranslationCalls && hasImport && !hasHookCall) {
      console.log(`  Adding hook to: ${filePath}`);
      
      // Find the first function/component and add the hook
      const lines = content.split('\n');
      let insertIndex = -1;
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // Look for function/component definitions
        if (/export\s+(?:const|function)\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{/.test(line) ||
            /function\s+\w+.*?\(.*?\).*?(?::\s*\w+.*?)?\s*{/.test(line) ||
            /const\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{/.test(line)) {
          
          // Insert the hook call after the opening brace
          insertIndex = i + 1;
          break;
        }
      }
      
      if (insertIndex !== -1) {
        // Find the proper indentation
        const nextLine = lines[insertIndex] || '';
        const indentation = nextLine.match(/^(\s*)/)[1];
        
        lines.splice(insertIndex, 0, `${indentation}const { t } = useTranslation();`);
        content = lines.join('\n');
        modified = true;
      }
    }

    if (modified) {
      fs.writeFileSync(fullPath, content);
      console.log(`  ✓ Fixed ${filePath}`);
      return true;
    } else {
      console.log(`  - No changes needed for ${filePath}`);
      return false;
    }

  } catch (error) {
    console.error(`  ✗ Error fixing ${filePath}:`, error.message);
    return false;
  }
}

// Main execution
console.log('Adding missing useTranslation hooks...\n');

let fixedCount = 0;
filesToFix.forEach(file => {
  if (addMissingHook(file)) {
    fixedCount++;
  }
});

console.log(`\nCompleted! Fixed ${fixedCount} out of ${filesToFix.length} files.`);
