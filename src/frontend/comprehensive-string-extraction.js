#!/usr/bin/env node

/**
 * COMPREHENSIVE STRING EXTRACTION FOR AXIESTUDIO
 * This script finds ALL hardcoded English strings and prepares them for Lingo.dev translation
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  sourceDir: 'src',
  outputFile: 'extracted-strings.json',
  translationFile: 'src/i18n/locales/en.json',
  excludeDirs: ['node_modules', 'build', 'dist', 'i18n', 'localized', '.git'],
  includeExtensions: ['.tsx', '.ts', '.jsx', '.js'],
  minStringLength: 3,
  maxStringLength: 200
};

// Patterns to find hardcoded strings
const STRING_PATTERNS = [
  // JSX text content: <span>Text here</span>
  />\s*([A-Z][^<>{}\n]*[a-z][^<>{}\n]*)\s*</g,
  
  // String literals in quotes: "Text here"
  /"([A-Z][^"\n]{2,}[a-z][^"\n]*)"/g,
  
  // Template literals: `Text here`
  /`([A-Z][^`\n]{2,}[a-z][^`\n]*)`/g,
  
  // Object property values: key: "Text here"
  /:\s*"([A-Z][^"\n]{2,}[a-z][^"\n]*)"/g,
  
  // Function call arguments: func("Text here")
  /\(\s*"([A-Z][^"\n]{2,}[a-z][^"\n]*)"\s*\)/g,
  
  // Array elements: ["Text here"]
  /\[\s*"([A-Z][^"\n]{2,}[a-z][^"\n]*)"\s*\]/g,
  
  // Constants: const TEXT = "Text here"
  /const\s+\w+\s*=\s*"([A-Z][^"\n]{2,}[a-z][^"\n]*)"/g,
];

// Strings to exclude (technical terms, URLs, etc.)
const EXCLUDE_PATTERNS = [
  /^https?:\/\//,           // URLs
  /^[A-Z_]+$/,              // ALL_CAPS constants
  /^\w+\.\w+/,              // file.extension
  /^[a-z]+[A-Z]/,           // camelCase
  /className|data-testid|aria-/,  // HTML attributes
  /console\.|import|export|from/, // Code keywords
  /\.(png|jpg|jpeg|gif|svg|css|js|ts|tsx|jsx)$/, // File extensions
  /^[0-9]/,                 // Starts with number
  /^\W/,                    // Starts with non-word character
];

// Found strings storage
const foundStrings = new Map();
const fileStats = {
  processed: 0,
  withStrings: 0,
  totalStrings: 0
};

function shouldProcessFile(filePath) {
  const ext = path.extname(filePath);
  const relativePath = path.relative(CONFIG.sourceDir, filePath);
  
  return CONFIG.includeExtensions.includes(ext) &&
         !CONFIG.excludeDirs.some(dir => relativePath.includes(dir)) &&
         !relativePath.includes('test') &&
         !relativePath.includes('spec');
}

function isValidString(str) {
  if (!str || str.length < CONFIG.minStringLength || str.length > CONFIG.maxStringLength) {
    return false;
  }
  
  // Check exclude patterns
  for (const pattern of EXCLUDE_PATTERNS) {
    if (pattern.test(str)) {
      return false;
    }
  }
  
  // Must contain at least one letter
  if (!/[a-zA-Z]/.test(str)) {
    return false;
  }
  
  // Must not be all uppercase (likely a constant)
  if (str === str.toUpperCase() && str.length > 3) {
    return false;
  }
  
  // Must not contain code-like patterns
  if (/[{}[\]();]/.test(str)) {
    return false;
  }
  
  return true;
}

function extractStringsFromFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const relativePath = path.relative(CONFIG.sourceDir, filePath);
    const stringsInFile = new Set();
    
    // Apply all string patterns
    for (const pattern of STRING_PATTERNS) {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        const str = match[1].trim();
        
        if (isValidString(str)) {
          stringsInFile.add(str);
          
          if (!foundStrings.has(str)) {
            foundStrings.set(str, {
              text: str,
              files: [],
              category: categorizeString(str),
              key: generateKey(str)
            });
          }
          
          foundStrings.get(str).files.push(relativePath);
        }
      }
    }
    
    fileStats.processed++;
    if (stringsInFile.size > 0) {
      fileStats.withStrings++;
      fileStats.totalStrings += stringsInFile.size;
      console.log(`📄 ${relativePath}: ${stringsInFile.size} strings`);
    }
    
    return stringsInFile.size;
    
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return 0;
  }
}

function categorizeString(str) {
  // Categorize strings for better organization
  if (/error|fail|invalid|wrong/i.test(str)) return 'errors';
  if (/button|click|press/i.test(str)) return 'buttons';
  if (/welcome|hello|hi/i.test(str)) return 'greetings';
  if (/save|delete|edit|add|create/i.test(str)) return 'actions';
  if (/loading|wait|process/i.test(str)) return 'status';
  if (/title|header|name/i.test(str)) return 'labels';
  if (/description|info|about/i.test(str)) return 'descriptions';
  if (/navigation|menu|page/i.test(str)) return 'navigation';
  if (/flow|component|node/i.test(str)) return 'flows';
  if (/file|upload|download/i.test(str)) return 'files';
  if (/user|admin|auth/i.test(str)) return 'auth';
  if (/chat|message|conversation/i.test(str)) return 'chat';
  if (/settings|config|preference/i.test(str)) return 'settings';
  
  return 'common';
}

function generateKey(str) {
  // Generate a translation key from the string
  return str
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .split(' ')
    .slice(0, 4) // Max 4 words
    .join('')
    .substring(0, 30); // Max 30 chars
}

function processDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    console.error(`❌ Directory not found: ${dirPath}`);
    return;
  }
  
  const items = fs.readdirSync(dirPath);
  
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      const relativePath = path.relative(CONFIG.sourceDir, fullPath);
      if (!CONFIG.excludeDirs.some(dir => relativePath.includes(dir))) {
        processDirectory(fullPath);
      }
    } else if (shouldProcessFile(fullPath)) {
      extractStringsFromFile(fullPath);
    }
  }
}

function generateTranslationFiles() {
  console.log('\n📝 Generating translation files...');
  
  // Group strings by category
  const categorizedStrings = {};
  
  for (const [text, data] of foundStrings) {
    const category = data.category;
    if (!categorizedStrings[category]) {
      categorizedStrings[category] = {};
    }
    
    // Create unique key within category
    let key = data.key;
    let counter = 1;
    while (categorizedStrings[category][key]) {
      key = `${data.key}${counter}`;
      counter++;
    }
    
    categorizedStrings[category][key] = text;
  }
  
  // Save extraction results
  const extractionResults = {
    timestamp: new Date().toISOString(),
    stats: fileStats,
    totalUniqueStrings: foundStrings.size,
    categories: Object.keys(categorizedStrings),
    strings: Array.from(foundStrings.values())
  };
  
  fs.writeFileSync(CONFIG.outputFile, JSON.stringify(extractionResults, null, 2));
  console.log(`✅ Extraction results saved to ${CONFIG.outputFile}`);
  
  // Update English translation file
  const existingTranslations = fs.existsSync(CONFIG.translationFile) 
    ? JSON.parse(fs.readFileSync(CONFIG.translationFile, 'utf8'))
    : {};
  
  // Merge with existing translations
  const mergedTranslations = { ...existingTranslations };
  
  for (const [category, strings] of Object.entries(categorizedStrings)) {
    if (!mergedTranslations[category]) {
      mergedTranslations[category] = {};
    }
    
    // Add new strings, preserve existing ones
    for (const [key, text] of Object.entries(strings)) {
      if (!mergedTranslations[category][key]) {
        mergedTranslations[category][key] = text;
      }
    }
  }
  
  // Ensure translation file directory exists
  const translationDir = path.dirname(CONFIG.translationFile);
  if (!fs.existsSync(translationDir)) {
    fs.mkdirSync(translationDir, { recursive: true });
  }
  
  fs.writeFileSync(CONFIG.translationFile, JSON.stringify(mergedTranslations, null, 2));
  console.log(`✅ Updated translation file: ${CONFIG.translationFile}`);
  
  return categorizedStrings;
}

function generateReport(categorizedStrings) {
  console.log('\n📊 EXTRACTION REPORT');
  console.log('='.repeat(50));
  console.log(`Files processed: ${fileStats.processed}`);
  console.log(`Files with strings: ${fileStats.withStrings}`);
  console.log(`Total unique strings: ${foundStrings.size}`);
  console.log(`Categories: ${Object.keys(categorizedStrings).length}`);
  
  console.log('\n📋 STRINGS BY CATEGORY:');
  for (const [category, strings] of Object.entries(categorizedStrings)) {
    console.log(`  ${category}: ${Object.keys(strings).length} strings`);
  }
  
  console.log('\n🔍 SAMPLE EXTRACTED STRINGS:');
  let count = 0;
  for (const [text, data] of foundStrings) {
    if (count >= 10) break;
    console.log(`  "${text}" → ${data.category}.${data.key}`);
    count++;
  }
  
  console.log('\n🎯 NEXT STEPS:');
  console.log('1. Review extracted-strings.json for accuracy');
  console.log('2. Run Lingo.dev to translate to Swedish');
  console.log('3. Replace hardcoded strings with t() calls');
  console.log('4. Test the application');
}

function main() {
  console.log('🔍 COMPREHENSIVE STRING EXTRACTION FOR AXIESTUDIO');
  console.log('Finding ALL hardcoded English strings...\n');
  
  // Process all files
  processDirectory(CONFIG.sourceDir);
  
  // Generate translation files
  const categorizedStrings = generateTranslationFiles();
  
  // Generate report
  generateReport(categorizedStrings);
  
  console.log(`\n🎉 Extraction complete! Found ${foundStrings.size} unique strings.`);
}

if (require.main === module) {
  main();
}

module.exports = { extractStringsFromFile, processDirectory, foundStrings };
