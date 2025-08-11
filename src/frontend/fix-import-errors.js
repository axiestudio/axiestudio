const fs = require('fs');
const path = require('path');

function fixImportErrors(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix duplicate import keywords
    const duplicateImportRegex = /import\s*{\s*import\s+/g;
    if (duplicateImportRegex.test(content)) {
      content = content.replace(duplicateImportRegex, 'import { ');
      modified = true;
    }
    
    // Fix import type issues
    const importTypeRegex = /import\s*{\s*import\s+type\s*{\s*/g;
    if (importTypeRegex.test(content)) {
      content = content.replace(importTypeRegex, 'import type { ');
      modified = true;
    }
    
    // Fix other import patterns
    const patterns = [
      { regex: /import\s*{\s*import\s+([^}]+)\s*}\s*from/g, replacement: 'import { $1 } from' },
      { regex: /import\s*{\s*import\s+([^,\s]+)/g, replacement: 'import { $1' },
      { regex: /import\s*{\s*import\s+type\s*{\s*([^}]+)\s*}\s*from/g, replacement: 'import type { $1 } from' }
    ];
    
    patterns.forEach(({ regex, replacement }) => {
      if (regex.test(content)) {
        content = content.replace(regex, replacement);
        modified = true;
      }
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed: ${filePath}`);
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
      if (fixImportErrors(fullPath)) {
        fixedCount++;
      }
    }
  });
  
  return fixedCount;
}

console.log('🔧 Fixing import errors...');
const fixedCount = walkDirectory('./src');
console.log(`🎉 Fixed ${fixedCount} files with import errors!`);
