const fs = require('fs');
const path = require('path');

/**
 * Fix syntax errors in JSX attributes caused by translation replacement
 */

function fixSyntaxErrors(content) {
  // Fix JSX attribute syntax: prop=t("key") -> prop={t("key")}
  content = content.replace(/(\w+)=t\(/g, '$1={t(');
  
  // Fix missing closing braces
  content = content.replace(/=\{t\("([^"]+)"\)(?!\})/g, '={t("$1")}');
  
  // Fix placeholder syntax: placeholder=t("key") -> placeholder={t("key")}
  content = content.replace(/(placeholder|title|icon|label|description|tooltip|aria-label)=t\(/g, '$1={t(');
  
  return content;
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    content = fixSyntaxErrors(content);
    
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

console.log('🔧 Fixing JSX syntax errors...');
processDirectory('src');
console.log('✅ Syntax fixes complete!');
