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
  // Look for t(" or t(' patterns, but exclude setTimeout, setInterval, etc.
  const matches = content.match(/\bt\s*\(\s*["'`]/g);
  if (!matches) return false;
  
  // Check if any of these are actual translation calls
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/\bt\s*\(\s*["'`]/.test(line) && 
        !line.includes('setTimeout') && 
        !line.includes('setInterval') && 
        !line.includes('clearTimeout') &&
        !line.includes('setT') &&
        !line.includes('getT') &&
        !line.includes('split(') &&
        !line.includes('createElement(') &&
        !line.includes('dispatchEvent(')) {
      return true;
    }
  }
  return false;
}

// Function to check if file has proper translation setup
function hasProperTranslationSetup(content) {
  const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
  const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)|const\s+t\s*=\s*useTranslation\s*\(\s*\)/.test(content);
  const takesTranslationParam = /\(\s*t\s*:\s*\(.*?\)\s*=>\s*string/.test(content);
  
  return (hasImport && hasHookCall) || takesTranslationParam;
}

// Main execution
console.log('Finding files with translation issues...');

const srcDir = path.join(__dirname, 'src');
const allFiles = findAllFiles(srcDir);

console.log(`Checking ${allFiles.length} TypeScript files...`);

const problematicFiles = [];

allFiles.forEach(file => {
  try {
    const content = fs.readFileSync(file, 'utf8');
    
    if (hasTranslationCalls(content) && !hasProperTranslationSetup(content)) {
      problematicFiles.push({
        file: file,
        relativePath: path.relative(srcDir, file)
      });
    }
  } catch (error) {
    // Skip files that can't be read
  }
});

console.log(`\nFound ${problematicFiles.length} files with translation issues:`);
problematicFiles.forEach(item => {
  console.log(`  ${item.relativePath}`);
});

if (problematicFiles.length > 0) {
  console.log('\nShowing first few files with their translation calls:');
  
  for (let i = 0; i < Math.min(5, problematicFiles.length); i++) {
    const item = problematicFiles[i];
    console.log(`\n--- ${item.relativePath} ---`);
    
    try {
      const content = fs.readFileSync(item.file, 'utf8');
      const lines = content.split('\n');
      
      lines.forEach((line, index) => {
        if (/\bt\s*\(\s*["'`]/.test(line) && 
            !line.includes('setTimeout') && 
            !line.includes('setInterval') && 
            !line.includes('clearTimeout') &&
            !line.includes('setT') &&
            !line.includes('getT') &&
            !line.includes('split(') &&
            !line.includes('createElement(') &&
            !line.includes('dispatchEvent(')) {
          console.log(`  Line ${index + 1}: ${line.trim()}`);
        }
      });
    } catch (error) {
      console.log(`  Error reading file: ${error.message}`);
    }
  }
}

console.log('\nDone.');
