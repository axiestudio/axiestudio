const fs = require('fs');
const path = require('path');

/**
 * Clean up duplicate and malformed imports
 */

function cleanImports(content) {
  // Remove duplicate useTranslation imports that were incorrectly inserted
  content = content.replace(/import\s*\{\s*import\s*\{\s*useTranslation\s*\}\s*from\s*['"]react-i18next['"];\s*/g, 'import {');
  
  // Fix malformed imports where useTranslation was inserted in the middle
  content = content.replace(/import\s*\{\s*useTranslation\s*\}\s*from\s*['"]react-i18next['"];\s*([^}]+)\s*\}/g, 'import { $1 }');
  
  // Remove standalone useTranslation imports in non-React files
  if (!content.includes('React') && !content.includes('JSX') && !content.includes('tsx')) {
    content = content.replace(/import\s*\{\s*useTranslation\s*\}\s*from\s*['"]react-i18next['"];\s*/g, '');
  }
  
  // Remove useTranslation hooks from non-component files
  if (!content.includes('React') && !content.includes('JSX') && !content.includes('tsx')) {
    content = content.replace(/const\s*\{\s*t\s*\}\s*=\s*useTranslation\(\);\s*/g, '');
  }
  
  return content;
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    content = cleanImports(content);
    
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Cleaned: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`❌ Error cleaning ${filePath}:`, error.message);
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

console.log('🧹 Cleaning up imports...');
processDirectory('src');
console.log('✅ Import cleanup complete!');
