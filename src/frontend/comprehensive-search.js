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

function analyzeFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Look for t(" or t(' patterns, but exclude common false positives
    const tCallMatches = content.match(/\bt\s*\(\s*["'`]/g);
    if (!tCallMatches) return null;
    
    // Filter out false positives
    const lines = content.split('\n');
    const actualTCalls = [];
    
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
          !line.includes('dispatchEvent(') &&
          !line.includes('getAttribute(') &&
          !line.includes('setAttribute(') &&
          !line.includes('removeAttribute(') &&
          !line.includes('hasAttribute(') &&
          !line.includes('querySelector(') &&
          !line.includes('querySelectorAll(') &&
          !line.includes('addEventListener(') &&
          !line.includes('removeEventListener(')) {
        actualTCalls.push({ lineNum: i + 1, line: line.trim() });
      }
    }
    
    if (actualTCalls.length === 0) return null;
    
    // Check translation setup
    const hasImport = /import.*useTranslation.*from.*react-i18next/.test(content);
    const hasHookCall = /const\s*{\s*t\s*}\s*=\s*useTranslation\s*\(\s*\)/.test(content);
    const takesTranslationParam = /\(\s*t\s*:\s*\(.*?\)\s*=>\s*string/.test(content);
    
    const hasProperSetup = (hasImport && hasHookCall) || takesTranslationParam;
    
    return {
      file: filePath,
      relativePath: path.relative(path.join(__dirname, 'src'), filePath),
      hasImport,
      hasHookCall,
      takesTranslationParam,
      hasProperSetup,
      tCalls: actualTCalls
    };
    
  } catch (error) {
    return null;
  }
}

// Main execution
console.log('Comprehensive search for translation issues...\n');

const srcDir = path.join(__dirname, 'src');
const allFiles = findAllFiles(srcDir);

console.log(`Analyzing ${allFiles.length} TypeScript files...`);

const results = [];
allFiles.forEach(file => {
  const analysis = analyzeFile(file);
  if (analysis) {
    results.push(analysis);
  }
});

console.log(`\nFound ${results.length} files with t() calls:`);

const problematicFiles = results.filter(r => !r.hasProperSetup);
const goodFiles = results.filter(r => r.hasProperSetup);

console.log(`\n✓ ${goodFiles.length} files have proper translation setup`);
console.log(`✗ ${problematicFiles.length} files have translation issues\n`);

if (problematicFiles.length > 0) {
  console.log('Files with issues:');
  problematicFiles.forEach(file => {
    console.log(`\n--- ${file.relativePath} ---`);
    console.log(`  Import: ${file.hasImport ? '✓' : '✗'}`);
    console.log(`  Hook: ${file.hasHookCall ? '✓' : '✗'}`);
    console.log(`  Param: ${file.takesTranslationParam ? '✓' : '✗'}`);
    console.log(`  Translation calls:`);
    file.tCalls.forEach(call => {
      console.log(`    Line ${call.lineNum}: ${call.line}`);
    });
  });
}

console.log('\nDone.');
