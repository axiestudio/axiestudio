#!/usr/bin/env node

/**
 * Comprehensive translation testing script
 * Tests both frontend and backend translation systems
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Configuration
const CONFIG = {
  frontend: {
    localesDir: 'src/frontend/src/i18n/locales',
    buildDir: 'src/frontend/build'
  },
  backend: {
    translationsDir: 'src/backend/translations',
    apiUrl: 'http://localhost:7860/api'
  },
  languages: ['en', 'sv']
};

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSection(title) {
  log(`\n${'='.repeat(60)}`, 'blue');
  log(`${title}`, 'bold');
  log(`${'='.repeat(60)}`, 'blue');
}

function logTest(name, passed, details = '') {
  const status = passed ? '✅ PASS' : '❌ FAIL';
  const color = passed ? 'green' : 'red';
  log(`${status} ${name}`, color);
  if (details) {
    log(`   ${details}`, 'yellow');
  }
}

// Test 1: Check translation files exist
function testTranslationFilesExist() {
  logSection('Testing Translation Files');
  
  let allPassed = true;
  
  // Check frontend translation files
  for (const lang of CONFIG.languages) {
    const frontendFile = path.join(CONFIG.frontend.localesDir, `${lang}.json`);
    const exists = fs.existsSync(frontendFile);
    logTest(`Frontend ${lang}.json exists`, exists, frontendFile);
    if (!exists) allPassed = false;
  }
  
  // Check backend translation files
  for (const lang of CONFIG.languages) {
    const backendFile = path.join(CONFIG.backend.translationsDir, `${lang}.json`);
    const exists = fs.existsSync(backendFile);
    logTest(`Backend ${lang}.json exists`, exists, backendFile);
    if (!exists) allPassed = false;
  }
  
  return allPassed;
}

// Test 2: Validate JSON structure
function testJSONStructure() {
  logSection('Testing JSON Structure');
  
  let allPassed = true;
  
  for (const lang of CONFIG.languages) {
    // Test frontend JSON
    try {
      const frontendFile = path.join(CONFIG.frontend.localesDir, `${lang}.json`);
      if (fs.existsSync(frontendFile)) {
        const content = JSON.parse(fs.readFileSync(frontendFile, 'utf8'));
        const keyCount = countKeys(content);
        logTest(`Frontend ${lang}.json valid JSON`, true, `${keyCount} keys`);
      }
    } catch (error) {
      logTest(`Frontend ${lang}.json valid JSON`, false, error.message);
      allPassed = false;
    }
    
    // Test backend JSON
    try {
      const backendFile = path.join(CONFIG.backend.translationsDir, `${lang}.json`);
      if (fs.existsSync(backendFile)) {
        const content = JSON.parse(fs.readFileSync(backendFile, 'utf8'));
        const keyCount = countKeys(content);
        logTest(`Backend ${lang}.json valid JSON`, true, `${keyCount} keys`);
      }
    } catch (error) {
      logTest(`Backend ${lang}.json valid JSON`, false, error.message);
      allPassed = false;
    }
  }
  
  return allPassed;
}

// Test 3: Check key consistency between languages
function testKeyConsistency() {
  logSection('Testing Key Consistency');
  
  let allPassed = true;
  
  // Test frontend key consistency
  try {
    const enFile = path.join(CONFIG.frontend.localesDir, 'en.json');
    const svFile = path.join(CONFIG.frontend.localesDir, 'sv.json');
    
    if (fs.existsSync(enFile) && fs.existsSync(svFile)) {
      const enKeys = getAllKeys(JSON.parse(fs.readFileSync(enFile, 'utf8')));
      const svKeys = getAllKeys(JSON.parse(fs.readFileSync(svFile, 'utf8')));
      
      const missingInSv = enKeys.filter(key => !svKeys.includes(key));
      const extraInSv = svKeys.filter(key => !enKeys.includes(key));
      
      logTest(
        'Frontend key consistency', 
        missingInSv.length === 0 && extraInSv.length === 0,
        `Missing in SV: ${missingInSv.length}, Extra in SV: ${extraInSv.length}`
      );
      
      if (missingInSv.length > 0) {
        log(`   Missing keys in Swedish: ${missingInSv.slice(0, 5).join(', ')}`, 'yellow');
        allPassed = false;
      }
    }
  } catch (error) {
    logTest('Frontend key consistency', false, error.message);
    allPassed = false;
  }
  
  // Test backend key consistency
  try {
    const enFile = path.join(CONFIG.backend.translationsDir, 'en.json');
    const svFile = path.join(CONFIG.backend.translationsDir, 'sv.json');
    
    if (fs.existsSync(enFile) && fs.existsSync(svFile)) {
      const enKeys = getAllKeys(JSON.parse(fs.readFileSync(enFile, 'utf8')));
      const svKeys = getAllKeys(JSON.parse(fs.readFileSync(svFile, 'utf8')));
      
      const missingInSv = enKeys.filter(key => !svKeys.includes(key));
      const extraInSv = svKeys.filter(key => !enKeys.includes(key));
      
      logTest(
        'Backend key consistency', 
        missingInSv.length === 0 && extraInSv.length === 0,
        `Missing in SV: ${missingInSv.length}, Extra in SV: ${extraInSv.length}`
      );
      
      if (missingInSv.length > 0) {
        log(`   Missing keys in Swedish: ${missingInSv.slice(0, 5).join(', ')}`, 'yellow');
        allPassed = false;
      }
    }
  } catch (error) {
    logTest('Backend key consistency', false, error.message);
    allPassed = false;
  }
  
  return allPassed;
}

// Test 4: Check for placeholder preservation
function testPlaceholderPreservation() {
  logSection('Testing Placeholder Preservation');
  
  let allPassed = true;
  
  try {
    const enFile = path.join(CONFIG.backend.translationsDir, 'en.json');
    const svFile = path.join(CONFIG.backend.translationsDir, 'sv.json');
    
    if (fs.existsSync(enFile) && fs.existsSync(svFile)) {
      const enContent = JSON.parse(fs.readFileSync(enFile, 'utf8'));
      const svContent = JSON.parse(fs.readFileSync(svFile, 'utf8'));
      
      const placeholderIssues = checkPlaceholders(enContent, svContent);
      
      logTest(
        'Placeholder preservation', 
        placeholderIssues.length === 0,
        `${placeholderIssues.length} issues found`
      );
      
      if (placeholderIssues.length > 0) {
        placeholderIssues.slice(0, 3).forEach(issue => {
          log(`   ${issue}`, 'yellow');
        });
        allPassed = false;
      }
    }
  } catch (error) {
    logTest('Placeholder preservation', false, error.message);
    allPassed = false;
  }
  
  return allPassed;
}

// Test 5: API endpoint testing
async function testAPIEndpoints() {
  logSection('Testing API Endpoints');
  
  let allPassed = true;
  
  const endpoints = [
    { path: '/health', method: 'GET' },
    { path: '/flows', method: 'GET' },
    { path: '/flows/999', method: 'GET' } // Should return 404
  ];
  
  for (const lang of CONFIG.languages) {
    for (const endpoint of endpoints) {
      try {
        const response = await axios({
          method: endpoint.method,
          url: `${CONFIG.backend.apiUrl}${endpoint.path}`,
          headers: {
            'Accept-Language': lang,
            'X-Language': lang
          },
          validateStatus: () => true // Don't throw on 4xx/5xx
        });
        
        const hasTranslatedContent = response.data && 
          (response.data.message || response.data.detail || response.data.error);
        
        logTest(
          `${endpoint.method} ${endpoint.path} (${lang})`, 
          hasTranslatedContent,
          `Status: ${response.status}, Content-Language: ${response.headers['content-language']}`
        );
        
        if (!hasTranslatedContent) allPassed = false;
        
      } catch (error) {
        logTest(
          `${endpoint.method} ${endpoint.path} (${lang})`, 
          false, 
          `Connection failed: ${error.message}`
        );
        allPassed = false;
      }
    }
  }
  
  return allPassed;
}

// Test 6: Frontend build verification
function testFrontendBuild() {
  logSection('Testing Frontend Build');
  
  const buildExists = fs.existsSync(CONFIG.frontend.buildDir);
  logTest('Frontend build exists', buildExists, CONFIG.frontend.buildDir);
  
  if (buildExists) {
    const indexExists = fs.existsSync(path.join(CONFIG.frontend.buildDir, 'index.html'));
    logTest('index.html exists', indexExists);
    
    if (indexExists) {
      const indexContent = fs.readFileSync(path.join(CONFIG.frontend.buildDir, 'index.html'), 'utf8');
      const hasI18nSupport = indexContent.includes('i18n') || indexContent.includes('translation');
      logTest('Build includes i18n support', hasI18nSupport);
      
      return indexExists && hasI18nSupport;
    }
  }
  
  return buildExists;
}

// Utility functions
function countKeys(obj, prefix = '') {
  let count = 0;
  for (const key in obj) {
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      count += countKeys(obj[key], `${prefix}${key}.`);
    } else {
      count++;
    }
  }
  return count;
}

function getAllKeys(obj, prefix = '') {
  let keys = [];
  for (const key in obj) {
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      keys = keys.concat(getAllKeys(obj[key], `${prefix}${key}.`));
    } else {
      keys.push(`${prefix}${key}`);
    }
  }
  return keys;
}

function checkPlaceholders(enObj, svObj, prefix = '') {
  const issues = [];
  
  for (const key in enObj) {
    const fullKey = `${prefix}${key}`;
    
    if (typeof enObj[key] === 'object' && enObj[key] !== null) {
      if (svObj[key]) {
        issues.push(...checkPlaceholders(enObj[key], svObj[key], `${fullKey}.`));
      }
    } else if (typeof enObj[key] === 'string') {
      const enPlaceholders = (enObj[key].match(/\{[^}]+\}/g) || []);
      const svPlaceholders = svObj[key] ? (svObj[key].match(/\{[^}]+\}/g) || []) : [];
      
      if (enPlaceholders.length !== svPlaceholders.length) {
        issues.push(`${fullKey}: Placeholder count mismatch (EN: ${enPlaceholders.length}, SV: ${svPlaceholders.length})`);
      }
    }
  }
  
  return issues;
}

// Main test runner
async function runAllTests() {
  log('🌍 Axiestudio Translation System Test Suite', 'bold');
  log('Testing comprehensive Swedish translation implementation\n');
  
  const results = {
    filesExist: testTranslationFilesExist(),
    jsonStructure: testJSONStructure(),
    keyConsistency: testKeyConsistency(),
    placeholders: testPlaceholderPreservation(),
    frontendBuild: testFrontendBuild(),
    apiEndpoints: await testAPIEndpoints()
  };
  
  // Summary
  logSection('Test Summary');
  
  const totalTests = Object.keys(results).length;
  const passedTests = Object.values(results).filter(Boolean).length;
  
  for (const [test, passed] of Object.entries(results)) {
    logTest(test, passed);
  }
  
  log(`\nOverall Result: ${passedTests}/${totalTests} tests passed`, 
    passedTests === totalTests ? 'green' : 'red');
  
  if (passedTests === totalTests) {
    log('\n🎉 All tests passed! Swedish translation system is working correctly.', 'green');
  } else {
    log('\n⚠️  Some tests failed. Please review the issues above.', 'yellow');
  }
  
  return passedTests === totalTests;
}

// Run tests if called directly
if (require.main === module) {
  runAllTests().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    log(`\n❌ Test suite failed: ${error.message}`, 'red');
    process.exit(1);
  });
}

module.exports = { runAllTests };
