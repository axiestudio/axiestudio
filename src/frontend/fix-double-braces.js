const fs = require('fs');
const path = require('path');

function fixDoubleBraces(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix double braces in imports like: import { { something } from
    const doubleBraceRegex = /import\s*{\s*{\s*([^}]+)\s*}\s*from/g;
    content = content.replace(doubleBraceRegex, (match, p1) => {
      modified = true;
      return `import { ${p1.trim()} } from`;
    });
    
    // Fix patterns like: import { { something, other } from
    const doubleBraceMultipleRegex = /import\s*{\s*{\s*([^}]+),\s*([^}]+)\s*}\s*from/g;
    content = content.replace(doubleBraceMultipleRegex, (match, p1, p2) => {
      modified = true;
      return `import { ${p1.trim()}, ${p2.trim()} } from`;
    });
    
    // Fix patterns like: import { { something, other, more } from
    const doubleBraceTripleRegex = /import\s*{\s*{\s*([^}]+),\s*([^}]+),\s*([^}]+)\s*}\s*from/g;
    content = content.replace(doubleBraceTripleRegex, (match, p1, p2, p3) => {
      modified = true;
      return `import { ${p1.trim()}, ${p2.trim()}, ${p3.trim()} } from`;
    });
    
    // Fix any remaining double braces patterns
    const generalDoubleBraceRegex = /import\s*{\s*{\s*([^}]*)\s*}\s*}/g;
    content = content.replace(generalDoubleBraceRegex, (match, p1) => {
      modified = true;
      return `import { ${p1.trim()} }`;
    });
    
    // Fix missing closing braces
    const missingCloseBraceRegex = /import\s*{\s*([^}]+)\s+from\s+/g;
    content = content.replace(missingCloseBraceRegex, (match, p1) => {
      if (!p1.includes('}')) {
        modified = true;
        return `import { ${p1.trim()} } from `;
      }
      return match;
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed double braces: ${filePath}`);
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
      if (fixDoubleBraces(fullPath)) {
        fixedCount++;
      }
    }
  });
  
  return fixedCount;
}

console.log('🔧 Fixing double brace syntax errors...');
const fixedCount = walkDirectory('./src');
console.log(`🎉 Fixed ${fixedCount} files with double brace errors!`);
