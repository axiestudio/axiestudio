const fs = require('fs');
const path = require('path');

function rapidFix(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix ALL the patterns we've seen:
    
    // 1. import { type { Something } from -> import type { Something } from
    if (content.includes('import { type {')) {
      content = content.replace(/import\s*{\s*type\s*{\s*([^}]+)\s*}\s*from/g, 'import type { $1 } from');
      modified = true;
    }
    
    // 2. import { import { -> import {
    if (content.includes('import { import {')) {
      content = content.replace(/import\s*{\s*import\s*{\s*([^}]+)\s*}\s*from/g, 'import { $1 } from');
      modified = true;
    }
    
    // 3. import Something } from -> import { Something } from
    if (content.match(/import\s+[A-Za-z_][A-Za-z0-9_]*\s*}\s*from/)) {
      content = content.replace(/import\s+([A-Za-z_][A-Za-z0-9_]*)\s*}\s*from/g, 'import { $1 } from');
      modified = true;
    }
    
    // 4. type { Something } from -> import type { Something } from
    if (content.match(/^\s*type\s*{\s*[^}]+\s*}\s*from/m)) {
      content = content.replace(/^(\s*)type\s*{\s*([^}]+)\s*}\s*from/gm, '$1import type { $2 } from');
      modified = true;
    }
    
    // 5. Clean up extra spaces and commas
    content = content.replace(/import\s*{\s*([^}]+),\s*}\s*from/g, 'import { $1 } from');
    content = content.replace(/import\s*{\s*([^}]+)\s*}\s*from/g, (match, imports) => {
      const cleanImports = imports.split(',').map(i => i.trim()).filter(i => i).join(', ');
      return `import { ${cleanImports} } from`;
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ ${filePath}`);
      return true;
    }
    return false;
  } catch (error) {
    console.error(`❌ ${filePath}: ${error.message}`);
    return false;
  }
}

function walkAndFix(dir) {
  const files = fs.readdirSync(dir);
  let count = 0;
  
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && !file.includes('node_modules')) {
      count += walkAndFix(fullPath);
    } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
      if (rapidFix(fullPath)) count++;
    }
  });
  
  return count;
}

console.log('🔥 RAPID FIX ALL SYNTAX ERRORS...');
const fixed = walkAndFix('./src');
console.log(`✅ Fixed ${fixed} files!`);
