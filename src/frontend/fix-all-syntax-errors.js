const fs = require('fs');
const path = require('path');

function fixAllSyntaxErrors(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix missing import keyword
    const missingImportRegex = /^(\s*)(type\s+[^,]+,\s*[^}]+}\s*from)/gm;
    content = content.replace(missingImportRegex, (match, whitespace, rest) => {
      modified = true;
      return `${whitespace}import { ${rest}`;
    });
    
    // Fix broken import statements with missing braces
    const brokenImportRegex = /import\s+([A-Za-z_][A-Za-z0-9_]*)\s*,\s*{\s*([^}]+)\s*}\s*from/g;
    content = content.replace(brokenImportRegex, (match, defaultImport, namedImports) => {
      modified = true;
      return `import ${defaultImport}, { ${namedImports} } from`;
    });
    
    // Fix double commas in imports
    const doubleCommaRegex = /import\s*{\s*([^}]+),\s*,\s*([^}]+)\s*}/g;
    content = content.replace(doubleCommaRegex, (match, p1, p2) => {
      modified = true;
      return `import { ${p1}, ${p2} }`;
    });
    
    // Fix malformed type imports
    const malformedTypeRegex = /import\s*{\s*type\s+([^,]+),\s*([^}]+)\s*}\s*from/g;
    content = content.replace(malformedTypeRegex, (match, typeImport, otherImports) => {
      modified = true;
      return `import { type ${typeImport}, ${otherImports} } from`;
    });
    
    // Fix missing useTranslation imports
    if (content.includes('useTranslation()') && !content.includes('import { useTranslation }')) {
      const reactImportMatch = content.match(/import\s+.*from\s+["']react["'];/);
      if (reactImportMatch) {
        const insertIndex = content.indexOf(reactImportMatch[0]) + reactImportMatch[0].length;
        content = content.slice(0, insertIndex) + '\nimport { useTranslation } from "react-i18next";' + content.slice(insertIndex);
        modified = true;
      }
    }
    
    // Fix extra spaces and formatting issues
    content = content.replace(/import\s*{\s*([^}]+)\s*}\s*from/g, (match, imports) => {
      const cleanImports = imports.split(',').map(imp => imp.trim()).join(', ');
      return `import { ${cleanImports} } from`;
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed syntax errors: ${filePath}`);
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
      if (fixAllSyntaxErrors(fullPath)) {
        fixedCount++;
      }
    }
  });
  
  return fixedCount;
}

console.log('🔧 Fixing all remaining syntax errors...');
const fixedCount = walkDirectory('./src');
console.log(`🎉 Fixed ${fixedCount} files with syntax errors!`);
