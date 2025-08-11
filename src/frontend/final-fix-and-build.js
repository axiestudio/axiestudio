const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔥 FINAL COMPREHENSIVE FIX AND BUILD SCRIPT');

function finalFixAllSyntax(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix ALL import statement patterns
    const patterns = [
      // Fix: import { something, import { type Other } from
      { 
        regex: /import\s*{\s*([^}]+),\s*import\s*{\s*([^}]+)\s*}\s*from/g, 
        replacement: 'import { $1, $2 } from' 
      },
      
      // Fix: type { Something } from (missing import)
      { 
        regex: /^(\s*)type\s*{\s*([^}]+)\s*}\s*from/gm, 
        replacement: '$1import type { $2 } from' 
      },
      
      // Fix: import { { Something } from (double braces)
      { 
        regex: /import\s*{\s*{\s*([^}]+)\s*}\s*from/g, 
        replacement: 'import { $1 } from' 
      },
      
      // Fix: import { something from (missing closing brace)
      { 
        regex: /import\s*{\s*([^}]+)\s+from\s+/g, 
        replacement: (match, p1) => {
          if (!p1.includes('}')) return `import { ${p1.trim()} } from `;
          return match;
        }
      },
      
      // Fix trailing commas and extra spaces
      { 
        regex: /import\s*{\s*([^}]+),\s*}\s*from/g, 
        replacement: 'import { $1 } from' 
      },
      
      // Clean up import formatting
      { 
        regex: /import\s*{\s*([^}]+)\s*}\s*from/g, 
        replacement: (match, p1) => {
          const cleanImports = p1.split(',').map(imp => imp.trim()).filter(imp => imp).join(', ');
          return `import { ${cleanImports} } from`;
        }
      }
    ];
    
    patterns.forEach(({ regex, replacement }) => {
      const oldContent = content;
      if (typeof replacement === 'function') {
        content = content.replace(regex, replacement);
      } else {
        content = content.replace(regex, replacement);
      }
      if (oldContent !== content) modified = true;
    });
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error fixing ${filePath}: ${error.message}`);
    return false;
  }
}

function walkDirectory(dir) {
  const files = fs.readdirSync(dir);
  let fixedCount = 0;
  
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && !file.includes('node_modules') && !file.includes('.git')) {
      fixedCount += walkDirectory(fullPath);
    } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
      if (finalFixAllSyntax(fullPath)) {
        fixedCount++;
      }
    }
  });
  
  return fixedCount;
}

// Keep trying until build succeeds or we've tried 5 times
let attempts = 0;
const maxAttempts = 5;

while (attempts < maxAttempts) {
  attempts++;
  console.log(`\n🔧 ATTEMPT ${attempts}/${maxAttempts}: Fixing syntax errors...`);
  
  const fixedCount = walkDirectory('./src');
  console.log(`✅ Fixed ${fixedCount} files in this attempt`);
  
  console.log('🔧 Attempting build...');
  try {
    execSync('npm run build', { stdio: 'inherit' });
    console.log('🎉 BUILD SUCCESSFUL!');
    
    console.log('🔧 Copying to backend...');
    execSync('Remove-Item -Recurse -Force "..\\..\\src\\backend\\base\\axiestudio\\frontend\\*" -ErrorAction SilentlyContinue', { shell: 'powershell', stdio: 'inherit' });
    execSync('Copy-Item -Recurse -Force "build\\*" "..\\..\\src\\backend\\base\\axiestudio\\frontend\\"', { shell: 'powershell', stdio: 'inherit' });
    console.log('🎉 FRONTEND WITH SWEDISH TRANSLATIONS COPIED TO BACKEND!');
    
    process.exit(0);
    
  } catch (error) {
    console.error(`❌ Build failed on attempt ${attempts}`);
    
    if (attempts === maxAttempts) {
      console.error('❌ Max attempts reached. Build still failing.');
      process.exit(1);
    }
    
    // Try to extract specific error and fix it
    try {
      const buildOutput = execSync('npm run build 2>&1', { encoding: 'utf8' });
      console.log('Build output for analysis:', buildOutput.substring(0, 1000));
    } catch (buildError) {
      const errorOutput = buildError.stdout || buildError.message;
      console.log('Build error for analysis:', errorOutput.substring(0, 1000));
      
      // Look for specific patterns in the error and fix them
      const errorMatch = errorOutput.match(/ERROR: (.+)/);
      if (errorMatch) {
        console.log(`🔧 Detected error pattern: ${errorMatch[1]}`);
      }
    }
  }
}
