const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔧 COMPREHENSIVE SYNTAX FIX AND BUILD SCRIPT');

function fixAllSyntaxIssues(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Fix all import statement issues
    const fixes = [
      // Fix double braces: import { { something } from
      { regex: /import\s*{\s*{\s*([^}]+)\s*}\s*from/g, replacement: 'import { $1 } from' },
      
      // Fix missing import keyword: type Something, other } from
      { regex: /^(\s*)(type\s+[^,]+,\s*[^}]+}\s*from)/gm, replacement: '$1import { $2' },
      
      // Fix broken imports: import { something from (missing closing brace)
      { regex: /import\s*{\s*([^}]+)\s+from\s+/g, replacement: (match, p1) => {
        if (!p1.includes('}')) return `import { ${p1.trim()} } from `;
        return match;
      }},
      
      // Fix trailing commas in imports
      { regex: /import\s*{\s*([^}]+),\s*}\s*from/g, replacement: 'import { $1 } from' },
      
      // Fix extra spaces
      { regex: /import\s*{\s*([^}]+)\s*}\s*from/g, replacement: (match, p1) => {
        const cleanImports = p1.split(',').map(imp => imp.trim()).filter(imp => imp).join(', ');
        return `import { ${cleanImports} } from`;
      }},
      
      // Fix malformed type imports
      { regex: /import\s*{\s*type\s+([^,]+),\s*([^}]+)\s*}\s*from/g, replacement: 'import { type $1, $2 } from' },
    ];
    
    fixes.forEach(({ regex, replacement }) => {
      if (typeof replacement === 'function') {
        content = content.replace(regex, replacement);
      } else {
        const oldContent = content;
        content = content.replace(regex, replacement);
        if (oldContent !== content) modified = true;
      }
    });
    
    // Add missing useTranslation imports where needed
    if (content.includes('useTranslation()') && !content.includes('import { useTranslation }')) {
      const reactImportMatch = content.match(/import\s+.*from\s+["']react["'];/);
      if (reactImportMatch) {
        const insertIndex = content.indexOf(reactImportMatch[0]) + reactImportMatch[0].length;
        content = content.slice(0, insertIndex) + '\nimport { useTranslation } from "react-i18next";' + content.slice(insertIndex);
        modified = true;
      }
    }
    
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
      if (fixAllSyntaxIssues(fullPath)) {
        fixedCount++;
      }
    }
  });
  
  return fixedCount;
}

console.log('🔧 Step 1: Fixing all syntax errors...');
const fixedCount = walkDirectory('./src');
console.log(`✅ Fixed ${fixedCount} files with syntax errors!`);

console.log('🔧 Step 2: Attempting build...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('🎉 BUILD SUCCESSFUL!');
  
  console.log('🔧 Step 3: Copying to backend...');
  execSync('Remove-Item -Recurse -Force "..\\..\\src\\backend\\base\\axiestudio\\frontend\\*" -ErrorAction SilentlyContinue', { shell: 'powershell', stdio: 'inherit' });
  execSync('Copy-Item -Recurse -Force "build\\*" "..\\..\\src\\backend\\base\\axiestudio\\frontend\\"', { shell: 'powershell', stdio: 'inherit' });
  console.log('🎉 FRONTEND COPIED TO BACKEND!');
  
} catch (error) {
  console.error('❌ Build failed:', error.message);
  console.log('🔧 Trying to fix remaining issues...');
  
  // Try to identify and fix specific build errors
  try {
    const buildOutput = execSync('npm run build 2>&1', { encoding: 'utf8' });
    console.log('Build output:', buildOutput);
  } catch (buildError) {
    console.log('Build error details:', buildError.stdout);
  }
}
