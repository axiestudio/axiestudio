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

// Function to check if content has translation calls
function hasTranslationCalls(content) {
  // Look for t(" or t(' patterns
  return /\bt\s*\(\s*["'`]/.test(content);
}

// Function to check if file has proper translation setup
function hasProperTranslationSetup(content) {
  const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
  const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)|const\s+t\s*=\s*useTranslation\s*\(\s*\)/.test(content);
  const takesTranslationParam = /\(\s*t\s*:\s*\(.*?\)\s*=>\s*string/.test(content);
  
  return (hasImport && hasHookCall) || takesTranslationParam;
}

// Function to determine if file should be a utility function
function shouldBeUtilityFunction(filePath, content) {
  return (
    filePath.includes('/helpers/') || 
    filePath.includes('/utils/') || 
    filePath.endsWith('.ts') ||
    /export\s+(?:const|function)\s+\w+.*=.*\(/.test(content)
  );
}

// Function to fix a single file
function fixFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    if (hasTranslationCalls(content) && !hasProperTranslationSetup(content)) {
      console.log(`Fixing: ${filePath}`);
      
      if (shouldBeUtilityFunction(filePath, content)) {
        // For utility functions, add t parameter
        const exportMatch = content.match(/(export\s+(?:const|function)\s+\w+)\s*=\s*\(/);
        if (exportMatch) {
          const beforeParen = exportMatch[1];
          const afterMatch = content.substring(content.indexOf(exportMatch[0]) + exportMatch[0].length);
          
          // Check if it already has parameters
          const hasParams = /^\s*\w+/.test(afterMatch);
          const newSignature = hasParams ? 
            `${beforeParen} = (t: (key: string) => string, ` :
            `${beforeParen} = (t: (key: string) => string`;
          
          content = content.replace(exportMatch[0], newSignature + '(');
          modified = true;
        }
      } else {
        // For React components, add useTranslation hook
        const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
        
        if (!hasImport) {
          // Add import at the top
          const firstImportMatch = content.match(/^import.*$/m);
          if (firstImportMatch) {
            content = content.replace(firstImportMatch[0], `import { useTranslation } from "react-i18next";\n${firstImportMatch[0]}`);
          } else {
            content = `import { useTranslation } from "react-i18next";\n${content}`;
          }
          modified = true;
        }
        
        // Add hook call to function/component
        const functionPatterns = [
          /(export\s+(?:const|function)\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{)/,
          /(function\s+\w+.*?\(.*?\).*?(?::\s*\w+.*?)?\s*{)/,
          /(const\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{)/
        ];
        
        for (const pattern of functionPatterns) {
          const functionMatch = content.match(pattern);
          if (functionMatch && !content.includes('const { t } = useTranslation();')) {
            const replacement = functionMatch[1] + '\n  const { t } = useTranslation();';
            content = content.replace(functionMatch[1], replacement);
            modified = true;
            break;
          }
        }
      }
      
      if (modified) {
        fs.writeFileSync(filePath, content);
        return true;
      }
    }
    
    return false;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    return false;
  }
}

// Main execution
console.log('Starting comprehensive translation fix...');

const srcDir = path.join(__dirname, 'src');
const allFiles = findAllFiles(srcDir);

console.log(`Found ${allFiles.length} TypeScript files`);

let fixedCount = 0;
let checkedCount = 0;

allFiles.forEach(file => {
  checkedCount++;
  if (fixFile(file)) {
    fixedCount++;
  }
  
  if (checkedCount % 100 === 0) {
    console.log(`Checked ${checkedCount}/${allFiles.length} files...`);
  }
});

console.log(`\nCompleted! Fixed ${fixedCount} files out of ${checkedCount} checked.`);
