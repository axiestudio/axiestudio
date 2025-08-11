#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Function to recursively find all TypeScript/TSX files
function findAllFiles(dir, fileList = []) {
  try {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      const filePath = path.join(dir, file);
      try {
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory()) {
          findAllFiles(filePath, fileList);
        } else if (file.endsWith('.tsx') || file.endsWith('.ts')) {
          fileList.push(filePath);
        }
      } catch (err) {
        // Skip files that can't be accessed
      }
    });
  } catch (err) {
    // Skip directories that can't be accessed
  }
  
  return fileList;
}

function fixMalformedFunction(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;

    // Check for malformed function signatures
    const malformedPattern = /export\s+const\s+(\w+)\s*=\s*\(t:\s*\(key:\s*string\)\s*=>\s*string\(\{/g;
    
    if (malformedPattern.test(content)) {
      console.log(`Fixing malformed function in: ${filePath}`);
      
      // Reset regex
      malformedPattern.lastIndex = 0;
      
      content = content.replace(malformedPattern, (match, functionName) => {
        modified = true;
        return `export const ${functionName} = ({`;
      });
      
      // Add useTranslation import if missing
      const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
      if (!hasImport) {
        const firstImportMatch = content.match(/^import.*$/m);
        if (firstImportMatch) {
          content = content.replace(firstImportMatch[0], `import { useTranslation } from "react-i18next";\n${firstImportMatch[0]}`);
        }
      }
      
      // Add hook call after function opening brace
      const functionMatch = content.match(/(export\s+const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{)/);
      if (functionMatch && !content.includes('const { t } = useTranslation();')) {
        const replacement = functionMatch[1] + '\n  const { t } = useTranslation();';
        content = content.replace(functionMatch[1], replacement);
      }
    }

    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`  ✓ Fixed ${filePath}`);
      return true;
    }
    
    return false;

  } catch (error) {
    console.error(`  ✗ Error fixing ${filePath}:`, error.message);
    return false;
  }
}

// Main execution
console.log('Finding and fixing all malformed function signatures...\n');

const srcDir = path.join(__dirname, 'src');
const allFiles = findAllFiles(srcDir);

console.log(`Checking ${allFiles.length} TypeScript files...`);

let fixedCount = 0;
allFiles.forEach(file => {
  if (fixMalformedFunction(file)) {
    fixedCount++;
  }
});

console.log(`\nCompleted! Fixed ${fixedCount} files with malformed function signatures.`);
