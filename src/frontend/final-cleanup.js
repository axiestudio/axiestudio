const fs = require('fs');
const path = require('path');

/**
 * Final cleanup script to fix all remaining syntax issues
 */

function finalCleanup(content) {
  // Fix malformed imports like "import { import { something"
  content = content.replace(/import\s*\{\s*import\s*\{\s*/g, 'import { ');
  
  // Fix malformed exports like "import { export function"
  content = content.replace(/import\s*\{\s*export\s+/g, 'export ');
  
  // Fix duplicate const declarations like "import { const something"
  content = content.replace(/import\s*\{\s*const\s+/g, 'const ');
  
  // Fix JSX attribute syntax issues
  content = content.replace(/(\w+)=t\(/g, '$1={t(');
  
  // Ensure proper closing braces for t() calls
  content = content.replace(/=\{t\("([^"]+)"\)(?!\})/g, '={t("$1")}');
  
  // Remove duplicate useTranslation imports
  const lines = content.split('\n');
  const seenImports = new Set();
  const cleanedLines = [];
  
  for (const line of lines) {
    if (line.includes('useTranslation') && line.includes('react-i18next')) {
      const importKey = line.trim();
      if (seenImports.has(importKey)) {
        continue; // Skip duplicate
      }
      seenImports.add(importKey);
    }
    cleanedLines.push(line);
  }
  
  return cleanedLines.join('\n');
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    content = finalCleanup(content);
    
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Final cleanup: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error cleaning ${filePath}:`, error.message);
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

console.log('🧹 Final cleanup of all syntax issues...');
processDirectory('src');
console.log('✅ Final cleanup complete!');
