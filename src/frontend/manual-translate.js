const fs = require('fs');
const https = require('https');

// Lingo.dev API configuration
const API_KEY = 'api_ikb8dilr97l4pt5hjnq0bunm';
const API_ENDPOINT = 'https://api.lingo.dev/v1/translate';

// Function to translate text using Lingo.dev API
async function translateText(text, sourceLang = 'en', targetLang = 'sv') {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      text: text,
      source_language: sourceLang,
      target_language: targetLang,
      context: 'software_ui',
      tone: 'professional',
      quality: 'high'
    });

    const options = {
      hostname: 'api.lingo.dev',
      port: 443,
      path: '/v1/translate',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (response.translated_text) {
            resolve(response.translated_text);
          } else {
            console.warn(`⚠️ No translation for: "${text}"`);
            resolve(text); // Return original if no translation
          }
        } catch (error) {
          console.error(`❌ Parse error for "${text}":`, error.message);
          resolve(text); // Return original on error
        }
      });
    });

    req.on('error', (error) => {
      console.error(`❌ Request error for "${text}":`, error.message);
      resolve(text); // Return original on error
    });

    req.write(postData);
    req.end();
  });
}

// Function to recursively translate object values
async function translateObject(obj, path = '') {
  const result = {};
  
  for (const [key, value] of Object.entries(obj)) {
    const currentPath = path ? `${path}.${key}` : key;
    
    if (typeof value === 'object' && value !== null) {
      console.log(`📁 Processing section: ${currentPath}`);
      result[key] = await translateObject(value, currentPath);
    } else if (typeof value === 'string') {
      // Skip very short strings or technical terms
      if (value.length < 3 || /^[a-z]+[A-Z]/.test(value) || /^[A-Z_]+$/.test(value)) {
        result[key] = value;
        continue;
      }
      
      console.log(`🔄 Translating: "${value}"`);
      try {
        const translated = await translateText(value);
        result[key] = translated;
        console.log(`✅ "${value}" → "${translated}"`);
        
        // Add small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error(`❌ Failed to translate "${value}":`, error.message);
        result[key] = value; // Keep original on error
      }
    } else {
      result[key] = value;
    }
  }
  
  return result;
}

// Main translation function
async function translateToSwedish() {
  try {
    console.log('🚀 Starting Swedish translation with Lingo.dev API...');
    
    // Read English translations
    const enPath = '../backend/translations/en.json';
    const svPath = '../backend/translations/sv.json';
    
    if (!fs.existsSync(enPath)) {
      throw new Error(`English translation file not found: ${enPath}`);
    }
    
    const englishTranslations = JSON.parse(fs.readFileSync(enPath, 'utf8'));
    console.log(`📖 Loaded English translations from: ${enPath}`);
    
    // Read existing Swedish translations
    let swedishTranslations = {};
    if (fs.existsSync(svPath)) {
      swedishTranslations = JSON.parse(fs.readFileSync(svPath, 'utf8'));
      console.log(`📖 Loaded existing Swedish translations from: ${svPath}`);
    }
    
    // Translate only new keys (those that don't exist in Swedish or are identical to English)
    console.log('🔍 Identifying new keys to translate...');
    const keysToTranslate = findKeysToTranslate(englishTranslations, swedishTranslations);
    console.log(`📝 Found ${keysToTranslate.length} keys to translate`);
    
    if (keysToTranslate.length === 0) {
      console.log('✅ All keys are already translated!');
      return;
    }
    
    // Translate new keys
    console.log('🌍 Starting translation process...');
    const translatedSwedish = await translateObject(englishTranslations);
    
    // Save updated Swedish translations
    fs.writeFileSync(svPath, JSON.stringify(translatedSwedish, null, 2));
    console.log(`✅ Swedish translations saved to: ${svPath}`);
    
    console.log('🎉 Translation complete!');
    
  } catch (error) {
    console.error('❌ Translation failed:', error.message);
    process.exit(1);
  }
}

// Helper function to find keys that need translation
function findKeysToTranslate(english, swedish, path = '') {
  const keysToTranslate = [];
  
  for (const [key, value] of Object.entries(english)) {
    const currentPath = path ? `${path}.${key}` : key;
    
    if (typeof value === 'object' && value !== null) {
      keysToTranslate.push(...findKeysToTranslate(value, swedish[key] || {}, currentPath));
    } else if (typeof value === 'string') {
      // Check if key needs translation
      if (!swedish[key] || swedish[key] === value) {
        keysToTranslate.push(currentPath);
      }
    }
  }
  
  return keysToTranslate;
}

// Run the translation
translateToSwedish();
