#!/usr/bin/env node

/**
 * SAFE AUTOMATED TRANSLATION SYSTEM FOR AXIESTUDIO
 * This script safely replaces hardcoded strings with translation calls
 * WITH COMPREHENSIVE SAFETY MEASURES TO PREVENT APP BREAKAGE
 */

const fs = require('fs');
const path = require('path');

// SAFETY CONFIGURATION
const SAFETY_CONFIG = {
  createBackups: true,
  validateSyntax: true,
  dryRun: false, // Set to true for testing
  maxFilesPerBatch: 50,
  skipCriticalFiles: [
    'node_modules',
    'build',
    'dist',
    'backup-',
    '.git',
    'package.json',
    'package-lock.json'
  ]
};

// Load extracted strings data
let extractedStrings = {};
try {
  const data = JSON.parse(fs.readFileSync('extracted-strings.json', 'utf8'));
  extractedStrings = data.strings.reduce((acc, item) => {
    acc[item.text] = `${item.category}.${item.key}`;
    return acc;
  }, {});
} catch (error) {
  console.error('❌ Could not load extracted strings:', error.message);
  process.exit(1);
}

// Statistics tracking
const stats = {
  filesProcessed: 0,
  filesModified: 0,
  stringsReplaced: 0,
  errors: 0,
  skipped: 0
};

// SAFETY FUNCTION: Create file backup
function createFileBackup(filePath) {
  if (!SAFETY_CONFIG.createBackups) return;
  
  const backupPath = `${filePath}.backup-${Date.now()}`;
  try {
    fs.copyFileSync(filePath, backupPath);
    return backupPath;
  } catch (error) {
    console.error(`⚠️  Could not create backup for ${filePath}:`, error.message);
    return null;
  }
}

// ENHANCED SYNTAX VALIDATION
function validateSyntax(content, filePath) {
  if (!SAFETY_CONFIG.validateSyntax) return true;

  try {
    // Count brackets and braces (excluding those in strings and comments)
    const cleanContent = removeStringsAndComments(content);

    const openBraces = (cleanContent.match(/\{/g) || []).length;
    const closeBraces = (cleanContent.match(/\}/g) || []).length;
    const openParens = (cleanContent.match(/\(/g) || []).length;
    const closeParens = (cleanContent.match(/\)/g) || []).length;
    const openBrackets = (cleanContent.match(/\[/g) || []).length;
    const closeBrackets = (cleanContent.match(/\]/g) || []).length;

    if (openBraces !== closeBraces) {
      console.error(`❌ Syntax error in ${filePath}: Mismatched braces (${openBraces} open, ${closeBraces} close)`);
      return false;
    }

    if (openParens !== closeParens) {
      console.error(`❌ Syntax error in ${filePath}: Mismatched parentheses (${openParens} open, ${closeParens} close)`);
      return false;
    }

    if (openBrackets !== closeBrackets) {
      console.error(`❌ Syntax error in ${filePath}: Mismatched brackets (${openBrackets} open, ${closeBrackets} close)`);
      return false;
    }

    // Check for problematic patterns
    const problematicPatterns = [
      { pattern: /t\(t\(/g, message: 'Nested t() calls detected' },
      { pattern: /t\(\s*\)/g, message: 'Empty t() calls detected' },
      { pattern: /t\(\s*""\s*\)/g, message: 'Empty string in t() calls detected' },
      { pattern: /\{\s*t\(\s*\)\s*\}/g, message: 'Empty t() in JSX detected' },
      { pattern: /import.*t\(/g, message: 'Translation call in import statement' },
      { pattern: /export.*t\(/g, message: 'Translation call in export statement' }
    ];

    for (const { pattern, message } of problematicPatterns) {
      if (pattern.test(content)) {
        console.error(`❌ Syntax error in ${filePath}: ${message}`);
        return false;
      }
    }

    return true;
  } catch (error) {
    console.error(`❌ Syntax validation failed for ${filePath}:`, error.message);
    return false;
  }
}

// Helper function to remove strings and comments for accurate bracket counting
function removeStringsAndComments(content) {
  return content
    // Remove single-line comments
    .replace(/\/\/.*$/gm, '')
    // Remove multi-line comments
    .replace(/\/\*[\s\S]*?\*\//g, '')
    // Remove string literals
    .replace(/"(?:[^"\\]|\\.)*"/g, '""')
    .replace(/'(?:[^'\\]|\\.)*'/g, "''")
    .replace(/`(?:[^`\\]|\\.)*`/g, '``');
}

// SAFETY FUNCTION: Check if file should be processed
function shouldProcessFile(filePath) {
  const relativePath = path.relative('src', filePath);
  
  // Skip critical files
  for (const skipPattern of SAFETY_CONFIG.skipCriticalFiles) {
    if (relativePath.includes(skipPattern)) {
      return false;
    }
  }
  
  // Only process specific extensions
  const ext = path.extname(filePath);
  if (!['.tsx', '.ts', '.jsx', '.js'].includes(ext)) {
    return false;
  }
  
  // Skip test files
  if (relativePath.includes('test') || relativePath.includes('spec')) {
    return false;
  }
  
  return true;
}

// IMPROVED SAFE STRING REPLACEMENT FUNCTION
function safeReplaceStrings(content, filePath) {
  let modifiedContent = content;
  let replacementCount = 0;

  // Sort strings by length (longest first) to avoid partial replacements
  const sortedStrings = Object.keys(extractedStrings).sort((a, b) => b.length - a.length);

  for (const originalString of sortedStrings) {
    const translationKey = extractedStrings[originalString];

    // Enhanced filtering for better safety
    if (!isStringSafeToReplace(originalString, content)) continue;

    // Create ultra-safe replacement patterns
    const patterns = [
      // JSX text content: >Text< (with better context checking)
      {
        pattern: new RegExp(`>\\s*${escapeRegex(originalString)}\\s*<`, 'g'),
        replacement: `>{t("${translationKey}")}<`,
        validate: (match, fullContent) => !match.includes('{') && !match.includes('}')
      },
      // String literals in simple contexts only
      {
        pattern: new RegExp(`(?<!\\w)"${escapeRegex(originalString)}"(?!\\w)`, 'g'),
        replacement: `t("${translationKey}")`,
        validate: (match, fullContent) => {
          // Don't replace if it's part of an import or complex expression
          const beforeMatch = fullContent.substring(0, fullContent.indexOf(match));
          const afterMatch = fullContent.substring(fullContent.indexOf(match) + match.length);
          return !beforeMatch.includes('import') &&
                 !beforeMatch.includes('from') &&
                 !afterMatch.startsWith('.') &&
                 !beforeMatch.endsWith('=');
        }
      },
      // Object property values (safer pattern)
      {
        pattern: new RegExp(`(\\w+):\\s*"${escapeRegex(originalString)}"`, 'g'),
        replacement: `$1: t("${translationKey}")`,
        validate: (match, fullContent) => !match.includes('import') && !match.includes('export')
      }
    ];

    for (const { pattern, replacement, validate } of patterns) {
      const matches = [...modifiedContent.matchAll(pattern)];

      for (const match of matches) {
        if (!validate || validate(match[0], modifiedContent)) {
          const beforeReplace = modifiedContent;
          modifiedContent = modifiedContent.replace(match[0], replacement.replace(/\$1/g, match[1] || ''));

          if (modifiedContent !== beforeReplace) {
            replacementCount++;
            console.log(`  ✅ "${originalString}" → t("${translationKey}")`);
          }
        }
      }
    }
  }

  return { content: modifiedContent, count: replacementCount };
}

// Enhanced string safety checker
function isStringSafeToReplace(str, content) {
  // Skip very short strings
  if (str.length < 4) return false;

  // Skip technical strings
  if (/^[a-z]+[A-Z]/.test(str)) return false; // camelCase
  if (/^[A-Z_]+$/.test(str)) return false; // CONSTANTS
  if (str.includes('.') && str.length < 20) return false; // file.ext
  if (/^\d/.test(str)) return false; // starts with number
  if (/^[^a-zA-Z]/.test(str)) return false; // starts with non-letter

  // Skip if it appears in imports or technical contexts
  const technicalContexts = [
    `import.*${escapeRegex(str)}`,
    `from.*${escapeRegex(str)}`,
    `export.*${escapeRegex(str)}`,
    `console\\..*${escapeRegex(str)}`,
    `className.*${escapeRegex(str)}`,
    `data-testid.*${escapeRegex(str)}`
  ];

  for (const context of technicalContexts) {
    if (new RegExp(context, 'i').test(content)) {
      return false;
    }
  }

  // Skip common technical terms
  const technicalTerms = [
    'Promise', 'Function', 'Object', 'Array', 'String', 'Number', 'Boolean',
    'React', 'Component', 'Props', 'State', 'Hook', 'Context',
    'TypeScript', 'JavaScript', 'HTML', 'CSS', 'JSON', 'XML',
    'API', 'HTTP', 'URL', 'URI', 'UUID', 'ID'
  ];

  if (technicalTerms.includes(str)) return false;

  return true;
}

// UTILITY: Escape regex special characters
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// SAFE IMPORT ADDITION
function addTranslationImport(content) {
  // Check if import already exists
  if (content.includes('useTranslation') || content.includes('from "react-i18next"')) {
    return content;
  }
  
  // Find the best place to add the import
  const importRegex = /import\s+.*?from\s+['"]react['"];?\s*\n/;
  const i18nImport = `import { useTranslation } from "react-i18next";\n`;
  
  if (importRegex.test(content)) {
    return content.replace(importRegex, (match) => `${match}${i18nImport}`);
  }
  
  // Add at the top if no React import found
  const firstImportRegex = /^(import\s+.*?;?\s*\n)/m;
  if (firstImportRegex.test(content)) {
    return content.replace(firstImportRegex, `$1${i18nImport}`);
  }
  
  return `${i18nImport}${content}`;
}

// SAFE HOOK ADDITION
function addTranslationHook(content) {
  // Check if hook already exists
  if (content.includes('const { t }') || content.includes('const {t}')) {
    return content;
  }
  
  // Find function component and add hook
  const functionPatterns = [
    /^(export\s+(?:default\s+)?(?:const|function)\s+\w+.*?\{)\s*$/m,
    /^(const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*\{)\s*$/m
  ];
  
  const hookDeclaration = `  const { t } = useTranslation();\n`;
  
  for (const pattern of functionPatterns) {
    if (pattern.test(content)) {
      return content.replace(pattern, `$1\n${hookDeclaration}`);
    }
  }
  
  return content;
}

// MAIN PROCESSING FUNCTION
function processFile(filePath) {
  try {
    stats.filesProcessed++;
    
    // Read original content
    const originalContent = fs.readFileSync(filePath, 'utf8');
    
    // Create backup
    const backupPath = createFileBackup(filePath);
    
    // Apply safe string replacements
    const { content: modifiedContent, count } = safeReplaceStrings(originalContent, filePath);
    
    // If no changes, skip
    if (modifiedContent === originalContent) {
      stats.skipped++;
      return;
    }
    
    // Add imports and hooks if strings were replaced
    let finalContent = modifiedContent;
    finalContent = addTranslationImport(finalContent);
    finalContent = addTranslationHook(finalContent);
    
    // Validate syntax before saving
    if (!validateSyntax(finalContent, filePath)) {
      console.error(`❌ Skipping ${filePath} due to syntax validation failure`);
      stats.errors++;
      return;
    }
    
    // Save changes (unless dry run)
    if (!SAFETY_CONFIG.dryRun) {
      fs.writeFileSync(filePath, finalContent, 'utf8');
    }
    
    stats.filesModified++;
    stats.stringsReplaced += count;
    
    console.log(`✅ Processed: ${path.relative('src', filePath)} (${count} strings replaced)`);
    
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    stats.errors++;
  }
}

// RECURSIVE DIRECTORY PROCESSING
function processDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) return;
  
  const items = fs.readdirSync(dirPath);
  
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      processDirectory(fullPath);
    } else if (shouldProcessFile(fullPath)) {
      processFile(fullPath);
      
      // Safety: Process in batches
      if (stats.filesProcessed % SAFETY_CONFIG.maxFilesPerBatch === 0) {
        console.log(`\n⏸️  Processed ${stats.filesProcessed} files. Pausing for safety check...`);
        console.log(`📊 Current stats: ${stats.filesModified} modified, ${stats.stringsReplaced} strings replaced, ${stats.errors} errors\n`);
      }
    }
  }
}

// MAIN EXECUTION
function main() {
  console.log('🛡️  SAFE AUTOMATED TRANSLATION SYSTEM');
  console.log('=====================================');
  console.log(`🔒 Safety mode: ${SAFETY_CONFIG.dryRun ? 'DRY RUN' : 'LIVE'}`);
  console.log(`📦 Backup creation: ${SAFETY_CONFIG.createBackups ? 'ENABLED' : 'DISABLED'}`);
  console.log(`🔍 Syntax validation: ${SAFETY_CONFIG.validateSyntax ? 'ENABLED' : 'DISABLED'}`);
  console.log(`📝 Strings to process: ${Object.keys(extractedStrings).length}`);
  console.log('=====================================\n');
  
  // Start processing
  processDirectory('src');
  
  // Final report
  console.log('\n🎉 TRANSLATION AUTOMATION COMPLETE!');
  console.log('===================================');
  console.log(`📁 Files processed: ${stats.filesProcessed}`);
  console.log(`✏️  Files modified: ${stats.filesModified}`);
  console.log(`🔄 Strings replaced: ${stats.stringsReplaced}`);
  console.log(`⏭️  Files skipped: ${stats.skipped}`);
  console.log(`❌ Errors: ${stats.errors}`);
  console.log('===================================');
  
  if (stats.errors > 0) {
    console.log('\n⚠️  Some files had errors. Please review the output above.');
  } else {
    console.log('\n✅ All files processed successfully!');
  }
}

if (require.main === module) {
  main();
}

module.exports = { processFile, processDirectory, stats };
