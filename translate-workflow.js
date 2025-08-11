#!/usr/bin/env node

/**
 * Complete Lingo.dev Translation Workflow for Axiestudio
 * Automates the entire translation process from string extraction to deployment
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const CONFIG = {
  frontend: {
    dir: 'src/frontend',
    i18nConfig: 'src/frontend/i18n.json',
    localesDir: 'src/frontend/src/i18n/locales',
    buildDir: 'src/frontend/build'
  },
  backend: {
    dir: 'src/backend',
    translationsDir: 'src/backend/translations'
  },
  lingo: {
    apiKey: 'api_ikb8dilr97l4pt5hjnq0bunm',
    batchSize: 50,
    quality: 'high'
  }
};

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logStep(step, message) {
  log(`\n🔄 Step ${step}: ${message}`, 'cyan');
}

function logSuccess(message) {
  log(`✅ ${message}`, 'green');
}

function logError(message) {
  log(`❌ ${message}`, 'red');
}

function logWarning(message) {
  log(`⚠️  ${message}`, 'yellow');
}

function execCommand(command, cwd = process.cwd()) {
  try {
    log(`   Running: ${command}`, 'blue');
    const result = execSync(command, { 
      cwd, 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.message, output: error.stdout };
  }
}

// Step 1: Setup and validation
function setupEnvironment() {
  logStep(1, 'Environment Setup and Validation');
  
  // Check if we're in the right directory
  if (!fs.existsSync('src/frontend') || !fs.existsSync('src/backend')) {
    logError('Please run this script from the Axiestudio root directory');
    process.exit(1);
  }
  
  // Check Node.js and npm
  const nodeCheck = execCommand('node --version');
  if (!nodeCheck.success) {
    logError('Node.js is not installed');
    process.exit(1);
  }
  logSuccess(`Node.js version: ${nodeCheck.output.trim()}`);
  
  // Check if Lingo.dev is installed
  const lingoCheck = execCommand('npx lingo.dev --version', CONFIG.frontend.dir);
  if (!lingoCheck.success) {
    log('   Installing Lingo.dev CLI...', 'yellow');
    const installResult = execCommand('npm install -g @lingo.dev/cli', CONFIG.frontend.dir);
    if (!installResult.success) {
      logError('Failed to install Lingo.dev CLI');
      process.exit(1);
    }
  }
  logSuccess('Lingo.dev CLI is available');
  
  // Verify API key
  if (!CONFIG.lingo.apiKey || CONFIG.lingo.apiKey === 'your_api_key_here') {
    logError('Please set your Lingo.dev API key in the configuration');
    process.exit(1);
  }
  logSuccess('Lingo.dev API key configured');
}

// Step 2: Extract frontend strings
function extractFrontendStrings() {
  logStep(2, 'Frontend String Extraction with Lingo.dev Compiler');
  
  // Ensure i18n.json exists
  if (!fs.existsSync(CONFIG.frontend.i18nConfig)) {
    logError('i18n.json configuration file not found');
    process.exit(1);
  }
  
  // Run Lingo.dev compiler
  const compilerResult = execCommand(
    'npx lingo.dev compiler --config i18n.json --verbose',
    CONFIG.frontend.dir
  );
  
  if (!compilerResult.success) {
    logError('Frontend string extraction failed');
    log(compilerResult.error, 'red');
    process.exit(1);
  }
  
  logSuccess('Frontend strings extracted successfully');
  
  // Check if localized directory was created
  const localizedDir = path.join(CONFIG.frontend.dir, 'src/localized');
  if (fs.existsSync(localizedDir)) {
    const files = fs.readdirSync(localizedDir);
    logSuccess(`Generated ${files.length} localized files`);
  }
}

// Step 3: Translate backend JSON files
function translateBackendFiles() {
  logStep(3, 'Backend Translation with Lingo.dev Bucket Mode');
  
  // Check if backend translation files exist
  const enFile = path.join(CONFIG.backend.translationsDir, 'en.json');
  if (!fs.existsSync(enFile)) {
    logError('Backend en.json file not found');
    process.exit(1);
  }
  
  // Run Lingo.dev i18n for backend translations
  const i18nResult = execCommand(
    'npx lingo.dev i18n --config i18n.json --verbose',
    CONFIG.frontend.dir
  );
  
  if (!i18nResult.success) {
    logWarning('Backend translation may have issues, but continuing...');
    log(i18nResult.error, 'yellow');
  } else {
    logSuccess('Backend translations updated successfully');
  }
  
  // Verify Swedish translations were created/updated
  const svFile = path.join(CONFIG.backend.translationsDir, 'sv.json');
  if (fs.existsSync(svFile)) {
    const svContent = JSON.parse(fs.readFileSync(svFile, 'utf8'));
    const keyCount = countKeys(svContent);
    logSuccess(`Swedish backend translations: ${keyCount} keys`);
  } else {
    logWarning('Swedish backend translations not found');
  }
}

// Step 4: Validate translations
function validateTranslations() {
  logStep(4, 'Translation Validation');
  
  let validationPassed = true;
  
  // Check frontend translations
  const frontendEn = path.join(CONFIG.frontend.localesDir, 'en.json');
  const frontendSv = path.join(CONFIG.frontend.localesDir, 'sv.json');
  
  if (fs.existsSync(frontendEn) && fs.existsSync(frontendSv)) {
    try {
      const enContent = JSON.parse(fs.readFileSync(frontendEn, 'utf8'));
      const svContent = JSON.parse(fs.readFileSync(frontendSv, 'utf8'));
      
      const enKeys = getAllKeys(enContent);
      const svKeys = getAllKeys(svContent);
      
      const missingKeys = enKeys.filter(key => !svKeys.includes(key));
      
      if (missingKeys.length === 0) {
        logSuccess(`Frontend translations complete: ${enKeys.length} keys`);
      } else {
        logWarning(`Frontend missing ${missingKeys.length} Swedish translations`);
        validationPassed = false;
      }
    } catch (error) {
      logError(`Frontend translation validation failed: ${error.message}`);
      validationPassed = false;
    }
  }
  
  // Check backend translations
  const backendEn = path.join(CONFIG.backend.translationsDir, 'en.json');
  const backendSv = path.join(CONFIG.backend.translationsDir, 'sv.json');
  
  if (fs.existsSync(backendEn) && fs.existsSync(backendSv)) {
    try {
      const enContent = JSON.parse(fs.readFileSync(backendEn, 'utf8'));
      const svContent = JSON.parse(fs.readFileSync(backendSv, 'utf8'));
      
      const enKeys = getAllKeys(enContent);
      const svKeys = getAllKeys(svContent);
      
      const missingKeys = enKeys.filter(key => !svKeys.includes(key));
      
      if (missingKeys.length === 0) {
        logSuccess(`Backend translations complete: ${enKeys.length} keys`);
      } else {
        logWarning(`Backend missing ${missingKeys.length} Swedish translations`);
        validationPassed = false;
      }
    } catch (error) {
      logError(`Backend translation validation failed: ${error.message}`);
      validationPassed = false;
    }
  }
  
  return validationPassed;
}

// Step 5: Build frontend with translations
function buildFrontend() {
  logStep(5, 'Building Frontend with Translations');
  
  // Install dependencies if needed
  if (!fs.existsSync(path.join(CONFIG.frontend.dir, 'node_modules'))) {
    log('   Installing frontend dependencies...', 'yellow');
    const installResult = execCommand('npm install', CONFIG.frontend.dir);
    if (!installResult.success) {
      logError('Failed to install frontend dependencies');
      process.exit(1);
    }
  }
  
  // Build the frontend
  const buildResult = execCommand('npm run build', CONFIG.frontend.dir);
  
  if (!buildResult.success) {
    logError('Frontend build failed');
    log(buildResult.error, 'red');
    process.exit(1);
  }
  
  logSuccess('Frontend built successfully with translations');
  
  // Check build output
  if (fs.existsSync(CONFIG.frontend.buildDir)) {
    const buildFiles = fs.readdirSync(CONFIG.frontend.buildDir);
    logSuccess(`Build contains ${buildFiles.length} files`);
  }
}

// Step 6: Copy build to backend
function deployToBackend() {
  logStep(6, 'Deploying Frontend Build to Backend');
  
  const backendFrontendDir = path.join(CONFIG.backend.dir, 'base/axiestudio/frontend');
  
  // Create backend frontend directory if it doesn't exist
  if (!fs.existsSync(backendFrontendDir)) {
    fs.mkdirSync(backendFrontendDir, { recursive: true });
  }
  
  // Copy build files
  const copyResult = execCommand(
    `xcopy "${CONFIG.frontend.buildDir}\\*" "${backendFrontendDir}" /E /Y /I`,
    process.cwd()
  );
  
  if (!copyResult.success) {
    // Try with PowerShell on Windows
    const psResult = execCommand(
      `powershell -Command "Copy-Item -Path '${CONFIG.frontend.buildDir}\\*' -Destination '${backendFrontendDir}' -Recurse -Force"`,
      process.cwd()
    );
    
    if (!psResult.success) {
      logError('Failed to copy build to backend');
      process.exit(1);
    }
  }
  
  logSuccess('Frontend build deployed to backend');
}

// Step 7: Generate summary report
function generateReport() {
  logStep(7, 'Generating Translation Report');
  
  const report = {
    timestamp: new Date().toISOString(),
    frontend: {},
    backend: {},
    summary: {}
  };
  
  // Frontend stats
  try {
    const frontendEn = path.join(CONFIG.frontend.localesDir, 'en.json');
    const frontendSv = path.join(CONFIG.frontend.localesDir, 'sv.json');
    
    if (fs.existsSync(frontendEn)) {
      const enContent = JSON.parse(fs.readFileSync(frontendEn, 'utf8'));
      report.frontend.englishKeys = getAllKeys(enContent).length;
    }
    
    if (fs.existsSync(frontendSv)) {
      const svContent = JSON.parse(fs.readFileSync(frontendSv, 'utf8'));
      report.frontend.swedishKeys = getAllKeys(svContent).length;
    }
  } catch (error) {
    report.frontend.error = error.message;
  }
  
  // Backend stats
  try {
    const backendEn = path.join(CONFIG.backend.translationsDir, 'en.json');
    const backendSv = path.join(CONFIG.backend.translationsDir, 'sv.json');
    
    if (fs.existsSync(backendEn)) {
      const enContent = JSON.parse(fs.readFileSync(backendEn, 'utf8'));
      report.backend.englishKeys = getAllKeys(enContent).length;
    }
    
    if (fs.existsSync(backendSv)) {
      const svContent = JSON.parse(fs.readFileSync(backendSv, 'utf8'));
      report.backend.swedishKeys = getAllKeys(svContent).length;
    }
  } catch (error) {
    report.backend.error = error.message;
  }
  
  // Summary
  report.summary.totalEnglishKeys = (report.frontend.englishKeys || 0) + (report.backend.englishKeys || 0);
  report.summary.totalSwedishKeys = (report.frontend.swedishKeys || 0) + (report.backend.swedishKeys || 0);
  report.summary.completionRate = report.summary.totalEnglishKeys > 0 
    ? Math.round((report.summary.totalSwedishKeys / report.summary.totalEnglishKeys) * 100)
    : 0;
  
  // Save report
  fs.writeFileSync('translation-report.json', JSON.stringify(report, null, 2));
  
  // Display summary
  log('\n📊 Translation Summary:', 'bold');
  log(`   Frontend: ${report.frontend.englishKeys || 0} EN → ${report.frontend.swedishKeys || 0} SV`);
  log(`   Backend:  ${report.backend.englishKeys || 0} EN → ${report.backend.swedishKeys || 0} SV`);
  log(`   Total:    ${report.summary.totalEnglishKeys} EN → ${report.summary.totalSwedishKeys} SV`);
  log(`   Completion: ${report.summary.completionRate}%`, 
    report.summary.completionRate >= 90 ? 'green' : 'yellow');
  
  logSuccess('Translation report saved to translation-report.json');
}

// Utility functions
function countKeys(obj) {
  let count = 0;
  for (const key in obj) {
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      count += countKeys(obj[key]);
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

// Main workflow
async function runTranslationWorkflow() {
  log('🌍 Axiestudio Swedish Translation Workflow', 'bold');
  log('Automated translation using Lingo.dev compiler + bucket mode\n');
  
  try {
    setupEnvironment();
    extractFrontendStrings();
    translateBackendFiles();
    const validationPassed = validateTranslations();
    buildFrontend();
    deployToBackend();
    generateReport();
    
    log('\n🎉 Translation workflow completed successfully!', 'green');
    
    if (!validationPassed) {
      logWarning('Some validation issues were found. Please review the report.');
    }
    
    log('\nNext steps:', 'bold');
    log('1. Start the Axiestudio server: uv run axiestudio run');
    log('2. Test the application with Swedish language');
    log('3. Run the test suite: node test-translations.js');
    
  } catch (error) {
    logError(`Workflow failed: ${error.message}`);
    process.exit(1);
  }
}

// Run workflow if called directly
if (require.main === module) {
  runTranslationWorkflow();
}

module.exports = { runTranslationWorkflow };
