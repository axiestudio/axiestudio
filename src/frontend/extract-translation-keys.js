const fs = require('fs');
const path = require('path');

// Function to extract translation keys from files
function extractTranslationKeys(directory) {
  const translationKeys = new Set();
  
  function scanDirectory(dir) {
    const files = fs.readdirSync(dir);
    
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        // Skip node_modules and other irrelevant directories
        if (!['node_modules', '.git', 'build', 'dist', 'backup-2025-08-10-2217'].includes(file)) {
          scanDirectory(filePath);
        }
      } else if (file.match(/\.(tsx?|jsx?)$/)) {
        // Read file content
        const content = fs.readFileSync(filePath, 'utf8');
        
        // Extract t("key") patterns
        const tFunctionMatches = content.match(/t\("([^"]+)"\)/g);
        if (tFunctionMatches) {
          tFunctionMatches.forEach(match => {
            const key = match.match(/t\("([^"]+)"\)/)[1];
            // Only add valid translation keys (must contain at least one letter and a dot)
            if (key && key.includes('.') && /[a-zA-Z]/.test(key) && key.length > 3) {
              translationKeys.add(key);
            }
          });
        }
      }
    }
  }
  
  scanDirectory(directory);
  return Array.from(translationKeys).sort();
}

// Function to create nested object from dot notation keys
function createNestedObject(keys) {
  const result = {};
  
  keys.forEach(key => {
    const parts = key.split('.');
    let current = result;
    
    for (let i = 0; i < parts.length - 1; i++) {
      if (!current[parts[i]]) {
        current[parts[i]] = {};
      }
      current = current[parts[i]];
    }
    
    // Set the final value (we'll use the key as placeholder for now)
    current[parts[parts.length - 1]] = key.split('.').pop().replace(/([A-Z])/g, ' $1').toLowerCase().trim();
  });
  
  return result;
}

// Extract keys from src directory
console.log('🔍 Extracting translation keys from frontend files...');
const keys = extractTranslationKeys('./src');

console.log(`✅ Found ${keys.length} translation keys:`);
keys.forEach(key => console.log(`  - ${key}`));

// Create nested object
const nestedTranslations = createNestedObject(keys);

// Read existing English translations
const enPath = '../backend/translations/en.json';
let existingEn = {};
if (fs.existsSync(enPath)) {
  existingEn = JSON.parse(fs.readFileSync(enPath, 'utf8'));
}

// Merge with existing translations
const mergedEn = { ...existingEn, ...nestedTranslations };

// Write updated English translations
fs.writeFileSync(enPath, JSON.stringify(mergedEn, null, 2));
console.log(`✅ Updated English translations: ${enPath}`);

// Read existing Swedish translations
const svPath = '../backend/translations/sv.json';
let existingSv = {};
if (fs.existsSync(svPath)) {
  existingSv = JSON.parse(fs.readFileSync(svPath, 'utf8'));
}

// Create Swedish translations with placeholders (to be translated by Lingo.dev)
const mergedSv = { ...existingSv, ...nestedTranslations };

// Write updated Swedish translations (with English placeholders for now)
fs.writeFileSync(svPath, JSON.stringify(mergedSv, null, 2));
console.log(`✅ Updated Swedish translations: ${svPath}`);

console.log('\n🎉 Translation key extraction complete!');
console.log('📝 Next step: Run Lingo.dev to translate the new keys to Swedish');
