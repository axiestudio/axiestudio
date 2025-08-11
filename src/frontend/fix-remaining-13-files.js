#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// List of remaining files that need fixing
const filesToFix = [
  'src/modals/deleteConfirmationModal/index.tsx',
  'src/modals/IOModal/components/chatView/chatInput/components/text-area-wrapper.tsx',
  'src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/language-select.tsx',
  'src/modals/IOModal/components/chatView/chatMessage/components/content-view.tsx',
  'src/modals/templatesModal/index.tsx',
  'src/pages/FlowPage/components/flowSidebarComponent/components/emptySearchComponent/index.tsx',
  'src/pages/FlowPage/components/flowSidebarComponent/components/featureTogglesComponent/index.tsx',
  'src/pages/FlowPage/components/flowSidebarComponent/components/searchInput/index.tsx',
  'src/pages/SettingsPage/pages/ApiKeysPage/components/ApiKeyHeader/index.tsx',
  'src/pages/SettingsPage/pages/GeneralPage/components/PasswordForm/index.tsx',
  'src/shared/components/textOutputView/index.tsx'
];

function fixFile(filePath) {
  try {
    const fullPath = path.join(__dirname, filePath);
    let content = fs.readFileSync(fullPath, 'utf8');
    let modified = false;

    console.log(`Fixing: ${filePath}`);

    // Check if it has translation calls
    const hasTranslationCalls = /\bt\s*\(\s*["'`]/.test(content);
    
    // Check if it has useTranslation import
    const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
    
    // Check if it has the hook call
    const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)/.test(content);

    if (hasTranslationCalls) {
      // Add import if missing
      if (!hasImport) {
        const firstImportMatch = content.match(/^import.*$/m);
        if (firstImportMatch) {
          content = content.replace(firstImportMatch[0], `import { useTranslation } from "react-i18next";\n${firstImportMatch[0]}`);
          modified = true;
        }
      }

      // Add hook call if missing
      if (!hasHookCall) {
        // Find function/component definition patterns
        const patterns = [
          /(export\s+(?:const|function)\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{)/,
          /(function\s+\w+.*?\(.*?\).*?(?::\s*\w+.*?)?\s*{)/,
          /(const\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{)/,
          /(export\s+default\s+function\s+\w+.*?\(.*?\).*?(?::\s*\w+.*?)?\s*{)/
        ];
        
        for (const pattern of patterns) {
          const functionMatch = content.match(pattern);
          if (functionMatch) {
            const replacement = functionMatch[1] + '\n  const { t } = useTranslation();';
            content = content.replace(functionMatch[1], replacement);
            modified = true;
            break;
          }
        }
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
console.log('Fixing remaining 11 files with translation issues...\n');

let fixedCount = 0;
filesToFix.forEach(file => {
  if (fixFile(file)) {
    fixedCount++;
  }
});

console.log(`\nCompleted! Fixed ${fixedCount} out of ${filesToFix.length} files.`);
