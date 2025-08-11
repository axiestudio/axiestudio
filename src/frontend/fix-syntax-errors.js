#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Files that need syntax fixes
const filesToFix = [
  'src/modals/secretKeyModal/components/content-render.tsx'
];

function fixSyntaxError(filePath) {
  try {
    const fullPath = path.join(__dirname, filePath);
    let content = fs.readFileSync(fullPath, 'utf8');
    let modified = false;

    console.log(`Fixing syntax in: ${filePath}`);

    // Fix malformed function signatures like: (t: (key: string) => string({params...
    // Should be: ({params...
    const malformedPattern = /export\s+const\s+(\w+)\s*=\s*\(t:\s*\(key:\s*string\)\s*=>\s*string\(\{([^}]+)\}/g;
    
    content = content.replace(malformedPattern, (match, functionName, params) => {
      console.log(`  Fixing malformed function: ${functionName}`);
      modified = true;
      return `export const ${functionName} = ({${params}}`;
    });

    // Add useTranslation import if missing and there are translation calls
    const hasTranslationCalls = /\bt\s*\(\s*["'`]/.test(content);
    const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
    
    if (hasTranslationCalls && !hasImport) {
      const firstImportMatch = content.match(/^import.*$/m);
      if (firstImportMatch) {
        content = content.replace(firstImportMatch[0], `import { useTranslation } from "react-i18next";\n${firstImportMatch[0]}`);
        modified = true;
      }
    }

    // Add hook call if missing
    const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)/.test(content);
    
    if (hasTranslationCalls && hasImport && !hasHookCall) {
      // Find function body and add hook
      const functionBodyMatch = content.match(/(export\s+const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{)/);
      if (functionBodyMatch) {
        const replacement = functionBodyMatch[1] + '\n  const { t } = useTranslation();';
        content = content.replace(functionBodyMatch[1], replacement);
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
console.log('Fixing syntax errors...\n');

let fixedCount = 0;
filesToFix.forEach(file => {
  if (fixSyntaxError(file)) {
    fixedCount++;
  }
});

console.log(`\nCompleted! Fixed ${fixedCount} out of ${filesToFix.length} files.`);
