const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function comprehensiveFix(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Pattern 1: useTranslation hook inside type definitions
    // export const Component: FC<{ const { t } = useTranslation(); prop: type }> = ({ prop }) => {
    const hookInTypeRegex = /export\s+const\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*FC<\s*{\s*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);\s*([^}]+)\s*}>\s*=\s*\(\s*{\s*([^}]+)\s*}\s*\)\s*=>\s*{/g;
    content = content.replace(hookInTypeRegex, (match, componentName, typeProps, destructuredProps) => {
      modified = true;
      return `export const ${componentName}: FC<{ ${typeProps.trim()} }> = ({ ${destructuredProps.trim()} }) => {\n  const { t } = useTranslation();`;
    });
    
    // Pattern 2: useTranslation hook inside function parameter types
    // function Component({ const { t } = useTranslation(); prop }: { prop: type }) {
    const hookInParamsRegex = /function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*{\s*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);\s*([^}]+)\s*}\s*:\s*{\s*([^}]+)\s*}\s*\)\s*{/g;
    content = content.replace(hookInParamsRegex, (match, funcName, destructuredProps, typeProps) => {
      modified = true;
      return `function ${funcName}({ ${destructuredProps.trim()} }: { ${typeProps.trim()} }) {\n  const { t } = useTranslation();`;
    });
    
    // Pattern 3: useTranslation hook interrupting destructuring
    // const { prop1, const { t } = useTranslation(); prop2 } = something;
    const hookInDestructuringRegex = /const\s*{\s*([^,]+),\s*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);\s*([^}]+)\s*}\s*=/g;
    content = content.replace(hookInDestructuringRegex, (match, prop1, prop2) => {
      modified = true;
      return `const { t } = useTranslation();\n  const { ${prop1.trim()}, ${prop2.trim()} } =`;
    });
    
    // Pattern 4: useTranslation hook inside object definitions
    // export const OBJECT = { const { t } = useTranslation(); prop: value }
    const hookInObjectRegex = /export\s+const\s+([A-Z_][A-Z0-9_]*)\s*=\s*{\s*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);\s*/g;
    content = content.replace(hookInObjectRegex, (match, objectName) => {
      modified = true;
      return `export const get${objectName} = (t: (key: string) => string) => ({\n  `;
    });
    
    // Pattern 5: Fix broken import statements
    const brokenImports = [
      { regex: /import\s*{\s*type\s*{\s*([^}]+)\s*}\s*from/g, replacement: 'import type { $1 } from' },
      { regex: /import\s*{\s*import\s*{\s*([^}]+)\s*}\s*from/g, replacement: 'import { $1 } from' },
      { regex: /import\s*{\s*\*\s*as\s+([^}]+)\s*}\s*from/g, replacement: 'import * as $1 from' },
      { regex: /import\s+([A-Za-z_][A-Za-z0-9_]*)\s*}\s*from/g, replacement: 'import { $1 } from' },
      { regex: /^(\s*)type\s*{\s*([^}]+)\s*}\s*from/gm, replacement: '$1import type { $2 } from' },
    ];
    
    brokenImports.forEach(({ regex, replacement }) => {
      const oldContent = content;
      content = content.replace(regex, replacement);
      if (oldContent !== content) modified = true;
    });
    
    // Pattern 6: Clean up duplicate useTranslation hooks
    const useTranslationMatches = content.match(/const\s*{\s*t\s*}\s*=\s*useTranslation\(\);/g);
    if (useTranslationMatches && useTranslationMatches.length > 1) {
      let count = 0;
      content = content.replace(/const\s*{\s*t\s*}\s*=\s*useTranslation\(\);/g, (match) => {
        count++;
        if (count === 1) return match;
        modified = true;
        return '';
      });
    }
    
    // Pattern 7: Fix malformed comments in imports
    content = content.replace(/import\s*{\s*\/\/[^}]*\s*export\s+const/g, (match) => {
      modified = true;
      return match.replace(/import\s*{\s*\/\/[^}]*/, '//');
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
      if (comprehensiveFix(fullPath)) count++;
    }
  });
  
  return count;
}

// Keep trying until build succeeds
let attempts = 0;
const maxAttempts = 20;

while (attempts < maxAttempts) {
  attempts++;
  console.log(`\n🔥 ATTEMPT ${attempts}: Comprehensive fix and build...`);
  
  const fixed = walkAndFix('./src');
  console.log(`✅ Fixed ${fixed} files`);
  
  try {
    console.log('🔧 Building...');
    execSync('npm run build', { stdio: 'pipe' });
    console.log('🎉 BUILD SUCCESSFUL!');
    
    console.log('🔧 Copying to backend...');
    execSync('Remove-Item -Recurse -Force "..\\..\\src\\backend\\base\\axiestudio\\frontend\\*" -ErrorAction SilentlyContinue', { shell: 'powershell' });
    execSync('Copy-Item -Recurse -Force "build\\*" "..\\..\\src\\backend\\base\\axiestudio\\frontend\\"', { shell: 'powershell' });
    console.log('🎉 SUCCESS! Swedish translations deployed to backend!');
    process.exit(0);
    
  } catch (error) {
    console.log(`❌ Build failed on attempt ${attempts}`);
    
    if (attempts === maxAttempts) {
      console.log('❌ Max attempts reached');
      process.exit(1);
    }
    
    // Extract specific error and try to fix it manually
    try {
      const buildOutput = execSync('npm run build 2>&1', { encoding: 'utf8' });
      const errorMatch = buildOutput.match(/ERROR: (.+)/);
      if (errorMatch) {
        console.log(`🔧 Error: ${errorMatch[1]}`);
        
        // Try to extract file and fix specific pattern
        const fileMatch = buildOutput.match(/file: ([^:]+):(\d+):(\d+)/);
        if (fileMatch) {
          const [, filePath, line, col] = fileMatch;
          console.log(`🔧 Fixing specific error in ${filePath} at line ${line}`);
          
          // Add specific fixes for common patterns
          try {
            let fileContent = fs.readFileSync(filePath, 'utf8');
            const lines = fileContent.split('\n');
            const errorLine = lines[parseInt(line) - 1];
            
            if (errorLine && errorLine.includes('const { t } = useTranslation();')) {
              // Move useTranslation hook to proper location
              lines[parseInt(line) - 1] = errorLine.replace(/const\s*{\s*t\s*}\s*=\s*useTranslation\(\);/, '');
              
              // Find the function body and add it there
              for (let i = parseInt(line); i < lines.length; i++) {
                if (lines[i].includes(') => {') || lines[i].includes(') {')) {
                  lines[i] = lines[i] + '\n  const { t } = useTranslation();';
                  break;
                }
              }
              
              fs.writeFileSync(filePath, lines.join('\n'));
              console.log(`✅ Fixed specific error in ${filePath}`);
            }
          } catch (fixError) {
            console.log(`❌ Could not fix specific error: ${fixError.message}`);
          }
        }
      }
    } catch (e) {
      console.log('Build error detected, trying again...');
    }
  }
}
