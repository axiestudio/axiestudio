const fs = require('fs');
const path = require('path');

function fixMissingImports(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix lines that start with "type {" - they should be "import type {"
    const missingImportTypeRegex = /^(\s*)type\s*{\s*([^}]+)\s*}\s*from/gm;
    content = content.replace(missingImportTypeRegex, (match, whitespace, typeImports) => {
      modified = true;
      return `${whitespace}import type { ${typeImports.trim()} } from`;
    });
    
    // Fix lines that have standalone type imports without import keyword
    const standaloneTypeRegex = /^(\s*)type\s+([A-Za-z_][A-Za-z0-9_]*)\s*,\s*([^}]+)\s*}\s*from/gm;
    content = content.replace(standaloneTypeRegex, (match, whitespace, firstType, rest) => {
      modified = true;
      return `${whitespace}import { type ${firstType}, ${rest} } from`;
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed missing imports: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error fixing ${filePath}: ${error.message}`);
    return false;
  }
}

function walkDirectory(dir) {
  const files = fs.readdirSync(dir);
  let fixedCount = 0;
  
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && !file.includes('node_modules') && !file.includes('.git')) {
      fixedCount += walkDirectory(fullPath);
    } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
      if (fixMissingImports(fullPath)) {
        fixedCount++;
      }
    }
  });
  
  return fixedCount;
}

console.log('🔧 Fixing missing import keywords...');
const fixedCount = walkDirectory('./src');
console.log(`✅ Fixed ${fixedCount} files with missing import keywords!`);
