#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Specific fixes for remaining files
const fixes = [
  {
    file: 'src/modals/IOModal/components/chatView/chatInput/components/text-area-wrapper.tsx',
    pattern: /(\}: TextAreaWrapperProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/language-select.tsx',
    pattern: /(\}: LanguageSelectProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/modals/IOModal/components/chatView/chatMessage/components/content-view.tsx',
    pattern: /(\}: ContentViewProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/pages/FlowPage/components/flowSidebarComponent/components/emptySearchComponent/index.tsx',
    pattern: /(\}: EmptySearchComponentProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/pages/FlowPage/components/flowSidebarComponent/components/featureTogglesComponent/index.tsx',
    pattern: /(\}: FeatureTogglesComponentProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/pages/FlowPage/components/flowSidebarComponent/components/searchInput/index.tsx',
    pattern: /(\}: SearchInputProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/pages/SettingsPage/pages/ApiKeysPage/components/ApiKeyHeader/index.tsx',
    pattern: /(\}: ApiKeyHeaderProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/pages/SettingsPage/pages/GeneralPage/components/PasswordForm/index.tsx',
    pattern: /(\}: PasswordFormProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  },
  {
    file: 'src/shared/components/textOutputView/index.tsx',
    pattern: /(\}: TextOutputViewProps\) => \{)/,
    replacement: '$1\n  const { t } = useTranslation();'
  }
];

function applyFix(fix) {
  try {
    const fullPath = path.join(__dirname, fix.file);
    let content = fs.readFileSync(fullPath, 'utf8');
    
    console.log(`Fixing: ${fix.file}`);
    
    // Check if it has translation calls
    const hasTranslationCalls = /\bt\s*\(\s*["'`]/.test(content);
    
    if (!hasTranslationCalls) {
      console.log(`  - No translation calls found in ${fix.file}`);
      return false;
    }
    
    // Check if it already has the hook
    const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)/.test(content);
    
    if (hasHookCall) {
      console.log(`  - Hook already exists in ${fix.file}`);
      return false;
    }
    
    // Apply the specific pattern fix
    if (fix.pattern.test(content)) {
      content = content.replace(fix.pattern, fix.replacement);
      fs.writeFileSync(fullPath, content);
      console.log(`  ✓ Fixed ${fix.file}`);
      return true;
    } else {
      // Try generic patterns
      const genericPatterns = [
        /(\) => \{)/,
        /(\): JSX\.Element \{)/,
        /(\) \{)/
      ];
      
      for (const pattern of genericPatterns) {
        if (pattern.test(content)) {
          content = content.replace(pattern, '$1\n  const { t } = useTranslation();');
          fs.writeFileSync(fullPath, content);
          console.log(`  ✓ Fixed ${fix.file} with generic pattern`);
          return true;
        }
      }
      
      console.log(`  - Pattern not found in ${fix.file}`);
      return false;
    }
    
  } catch (error) {
    console.error(`  ✗ Error fixing ${fix.file}:`, error.message);
    return false;
  }
}

// Main execution
console.log('Applying manual fixes to remaining files...\n');

let fixedCount = 0;
fixes.forEach(fix => {
  if (applyFix(fix)) {
    fixedCount++;
  }
});

console.log(`\nCompleted! Fixed ${fixedCount} out of ${fixes.length} files.`);
