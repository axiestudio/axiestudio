#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Function to recursively find all TypeScript/TSX files
function findTsFiles(dir, fileList = []) {
  try {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
      const filePath = path.join(dir, file);
      try {
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
          findTsFiles(filePath, fileList);
        } else if (file.endsWith('.tsx') || file.endsWith('.ts')) {
          fileList.push(filePath);
        }
      } catch (err) {
        console.log(`Skipping ${filePath}: ${err.message}`);
      }
    });
  } catch (err) {
    console.log(`Cannot read directory ${dir}: ${err.message}`);
  }

  return fileList;
}

// Function to check if file has translation calls
function hasTranslationCalls(content) {
  return /\bt\s*\(\s*["'`]/.test(content);
}

// Function to check if file has proper useTranslation setup
function hasProperTranslationSetup(content) {
  const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
  const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)|const\s+t\s*=\s*useTranslation\s*\(\s*\)/.test(content);
  const isUtilityFunction = /export\s+(?:const|function)\s+\w+.*=.*\(.*t\s*:/.test(content);

  return (hasImport && hasHookCall) || isUtilityFunction;
}

// Function to fix a single file
function fixFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;

    if (hasTranslationCalls(content) && !hasProperTranslationSetup(content)) {
      console.log(`Fixing: ${filePath}`);

      // Check if it's a utility function that should take t as parameter
      const isUtilityFile = filePath.includes('/helpers/') || filePath.includes('/utils/') || filePath.endsWith('.ts');

      if (isUtilityFile && !filePath.includes('hooks/')) {
        // For utility files, convert to take t as parameter
        const exportMatch = content.match(/(export\s+(?:const|function)\s+\w+)\s*=\s*\(\s*\)\s*=>/);
        if (exportMatch) {
          content = content.replace(exportMatch[0], `${exportMatch[1]} = (t: (key: string) => string) =>`);
          modified = true;
        }
      } else {
        // For React components, add useTranslation hook
        const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);

        if (!hasImport) {
          content = `import { useTranslation } from "react-i18next";\n${content}`;
          modified = true;
        }

        // Find component/function and add hook call
        const patterns = [
          /(export\s+(?:const|function)\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{)/,
          /(function\s+\w+.*?\(.*?\).*?(?::\s*\w+.*?)?\s*{)/,
          /(const\s+\w+.*?=.*?\(.*?\).*?(?::\s*\w+.*?)?\s*(?:=>)?\s*{)/
        ];

        for (const pattern of patterns) {
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

// Function to find files with translation calls using grep
function findFilesWithTranslationCalls() {
  try {
    const result = execSync('grep -r "t(\\"\\|t(\'" src/ --include="*.tsx" --include="*.ts" -l', { encoding: 'utf8' });
    return result.trim().split('\n').filter(line => line.trim());
  } catch (error) {
    console.log('Grep command failed, falling back to manual search');
    return [];
  }
}

// Main execution
console.log('Finding files with translation calls...');
const filesWithTranslations = findFilesWithTranslationCalls();
console.log(`Found ${filesWithTranslations.length} files with translation calls`);

const srcDir = path.join(__dirname, 'src');
const allTsFiles = findTsFiles(srcDir);
console.log(`Found ${allTsFiles.length} total TypeScript files`);

// Combine both approaches
const filesToCheck = new Set([...filesWithTranslations, ...allTsFiles]);

let fixedCount = 0;
filesToCheck.forEach(file => {
  if (fixFile(file)) {
    fixedCount++;
  }
});

console.log(`Fixed ${fixedCount} files`);
