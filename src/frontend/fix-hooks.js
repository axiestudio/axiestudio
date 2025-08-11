const fs = require('fs');
const path = require('path');

/**
 * Fix misplaced useTranslation hooks in function parameters
 */

function fixHookPlacement(content) {
  // Fix hooks that were inserted in function parameters
  // Pattern: function({const { t } = useTranslation(); param1, param2})
  content = content.replace(
    /(\w+\s*\(\s*\{)\s*const\s*\{\s*t\s*\}\s*=\s*useTranslation\(\);\s*/g,
    '$1'
  );
  
  // Fix hooks that were inserted before function body starts
  // Pattern: }: Type): ReturnType {\nconst { t } = useTranslation();\n
  content = content.replace(
    /(}\s*:\s*\w+.*?\)\s*:\s*\w+.*?\s*\{)\s*(const\s*\{\s*t\s*\}\s*=\s*useTranslation\(\);\s*)?/g,
    (match, funcStart, hook) => {
      if (hook) {
        return funcStart + '\n  ' + hook.trim() + '\n';
      }
      return match;
    }
  );
  
  return content;
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    content = fixHookPlacement(content);
    
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Fixed hooks: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error fixing ${filePath}:`, error.message);
    return false;
  }
}

function processDirectory(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return;
  }
  
  const items = fs.readdirSync(dirPath);
  
  for (const item of items) {
    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      processDirectory(fullPath);
    } else if (fullPath.endsWith('.tsx') || fullPath.endsWith('.ts')) {
      processFile(fullPath);
    }
  }
}

console.log('🔧 Fixing hook placement...');
processDirectory('src');
console.log('✅ Hook fixes complete!');
