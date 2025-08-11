const fs = require('fs');
const path = require('path');

/**
 * Comprehensive fix for all translation-related syntax issues
 */

function fixAllIssues(content) {
  // Remove hooks from function parameters
  content = content.replace(
    /(\w+\s*=\s*\(\s*\{)\s*const\s*\{\s*t\s*\}\s*=\s*useTranslation\(\);\s*/g,
    '$1'
  );
  
  // Remove hooks from arrow function parameters
  content = content.replace(
    /(export\s+const\s+\w+\s*=\s*\(\s*\{)\s*const\s*\{\s*t\s*\}\s*=\s*useTranslation\(\);\s*/g,
    '$1'
  );
  
  // Fix JSX attribute syntax
  content = content.replace(/(\w+)=t\(/g, '$1={t(');
  content = content.replace(/=\{t\("([^"]+)"\)(?!\})/g, '={t("$1")}');
  
  // Ensure hooks are properly placed in function bodies
  // For arrow functions: }) => {\n  const { t } = useTranslation();
  content = content.replace(
    /(}\)\s*=>\s*\{)(\s*)((?!.*const\s*\{\s*t\s*\}.*useTranslation))/,
    '$1\n  const { t } = useTranslation();$2$3'
  );
  
  // For regular functions: ): Type {\n  const { t } = useTranslation();
  content = content.replace(
    /(}\s*:\s*\w+.*?\)\s*:\s*\w+.*?\s*\{)(\s*)((?!.*const\s*\{\s*t\s*\}.*useTranslation))/,
    '$1\n  const { t } = useTranslation();$2$3'
  );
  
  return content;
}

function ensureTranslationImport(content) {
  // Check if useTranslation is already imported
  if (content.includes('useTranslation') && content.includes('react-i18next')) {
    return content;
  }
  
  // Check if we need to add the import (only if t() is used)
  if (!content.includes('t(')) {
    return content;
  }
  
  // Find React imports and add useTranslation
  const reactImportRegex = /import\s+.*from\s+['"]react['"];?/;
  const i18nImport = `import { useTranslation } from 'react-i18next';`;
  
  if (reactImportRegex.test(content)) {
    return content.replace(reactImportRegex, (match) => `${match}\n${i18nImport}`);
  }
  
  // If no React import, add at the top after other imports
  const firstImportRegex = /^(import\s+.*?;?\s*\n)/m;
  if (firstImportRegex.test(content)) {
    return content.replace(firstImportRegex, `$1${i18nImport}\n`);
  }
  
  // If no imports, add at the very top
  return `${i18nImport}\n${content}`;
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    // Apply all fixes
    content = fixAllIssues(content);
    content = ensureTranslationImport(content);
    
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Fixed: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error fixing ${filePath}:`, error.message);
    return false;
  }
}

function processDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return;
  }
  
  const items = fs.readdirSync(dirPath);
  
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      processDirectory(fullPath);
    } else if (fullPath.endsWith('.tsx') || fullPath.endsWith('.ts')) {
      processFile(fullPath);
    }
  }
}

console.log('🔧 Fixing all translation issues...');
processDirectory('src');
console.log('✅ All fixes complete!');
