const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function ultimateFix(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix ALL import patterns we've encountered:
    
    // 1. import { * as Something } -> import * as Something
    if (content.includes('import { * as ')) {
      content = content.replace(/import\s*{\s*\*\s*as\s+([^}]+)\s*}\s*from/g, 'import * as $1 from');
      modified = true;
    }
    
    // 2. import { type { Something } -> import type { Something
    if (content.includes('import { type {')) {
      content = content.replace(/import\s*{\s*type\s*{\s*([^}]+)\s*}\s*from/g, 'import type { $1 } from');
      modified = true;
    }
    
    // 3. import { import { -> import {
    if (content.includes('import { import {')) {
      content = content.replace(/import\s*{\s*import\s*{\s*([^}]+)\s*}\s*from/g, 'import { $1 } from');
      modified = true;
    }
    
    // 4. Duplicate useTranslation hooks
    const useTranslationMatches = content.match(/const\s*{\s*t\s*}\s*=\s*useTranslation\(\);/g);
    if (useTranslationMatches && useTranslationMatches.length > 1) {
      // Keep only the first one
      let count = 0;
      content = content.replace(/const\s*{\s*t\s*}\s*=\s*useTranslation\(\);/g, (match) => {
        count++;
        return count === 1 ? match : '';
      });
      modified = true;
    }
    
    // 5. useTranslation hook in wrong place (inside function parameters)
    if (content.includes('export default function') && content.includes('const { t } = useTranslation();')) {
      // Check if useTranslation is inside function parameters
      const funcMatch = content.match(/(export default function [^{]+\{[^}]*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);[^}]*\})/);
      if (funcMatch) {
        // Move useTranslation to inside function body
        content = content.replace(
          /(export default function [^{]+\{)\s*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);\s*([^}]+\}[^{]*\{)/,
          '$1$2\n  const { t } = useTranslation();\n'
        );
        modified = true;
      }
    }
    
    // 6. Fix missing braces in imports
    content = content.replace(/import\s+([A-Za-z_][A-Za-z0-9_]*)\s*}\s*from/g, 'import { $1 } from');
    
    // 7. Fix type imports without import keyword
    content = content.replace(/^(\s*)type\s*{\s*([^}]+)\s*}\s*from/gm, '$1import type { $2 } from');
    
    // 8. Clean up extra commas and spaces
    content = content.replace(/import\s*{\s*([^}]+),\s*}\s*from/g, 'import { $1 } from');
    content = content.replace(/import\s*{\s*([^}]+)\s*}\s*from/g, (match, imports) => {
      const cleanImports = imports.split(',').map(i => i.trim()).filter(i => i).join(', ');
      return `import { ${cleanImports} } from`;
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ ${filePath}`);
      return true;
    }
    return false;
  } catch (error) {
    console.error(`❌ ${filePath}: ${error.message}`);
    return false;
  }
}

function walkAndFix(dir) {
  const files = fs.readdirSync(dir);
  let count = 0;
  
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && !file.includes('node_modules')) {
      count += walkAndFix(fullPath);
    } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
      if (ultimateFix(fullPath)) count++;
    }
  });
  
  return count;
}

// Keep trying until build succeeds
let attempts = 0;
const maxAttempts = 10;

while (attempts < maxAttempts) {
  attempts++;
  console.log(`\n🔥 ATTEMPT ${attempts}: Ultimate fix and build...`);
  
  const fixed = walkAndFix('./src');
  console.log(`✅ Fixed ${fixed} files`);
  
  try {
    console.log('🔧 Building...');
    execSync('npm run build', { stdio: 'pipe' });
    console.log('🎉 BUILD SUCCESSFUL!');
    
    console.log('🔧 Copying to backend...');
    execSync('Remove-Item -Recurse -Force "..\\..\\src\\backend\\base\\axiestudio\\frontend\\*" -ErrorAction SilentlyContinue', { shell: 'powershell' });
    execSync('Copy-Item -Recurse -Force "build\\*" "..\\..\\src\\backend\\base\\axiestudio\\frontend\\"', { shell: 'powershell' });
    console.log('🎉 SUCCESS! Frontend with Swedish translations deployed!');
    process.exit(0);
    
  } catch (error) {
    console.log(`❌ Build failed on attempt ${attempts}`);
    
    if (attempts === maxAttempts) {
      console.log('❌ Max attempts reached');
      process.exit(1);
    }
    
    // Extract and show the specific error
    try {
      const buildOutput = execSync('npm run build 2>&1', { encoding: 'utf8' });
      const errorMatch = buildOutput.match(/ERROR: (.+)/);
      if (errorMatch) {
        console.log(`🔧 Error: ${errorMatch[1]}`);
      }
    } catch (e) {
      console.log('Build error detected, trying again...');
    }
  }
}
