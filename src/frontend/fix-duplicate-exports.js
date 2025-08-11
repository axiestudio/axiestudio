const fs = require('fs');
const path = require('path');

console.log('🔧 FIXING ALL DUPLICATE EXPORT ISSUES...\n');

// Function to recursively find all TypeScript/JavaScript files
function findAllFiles(dir, extensions = ['.tsx', '.ts', '.jsx', '.js']) {
  let results = [];
  
  if (!fs.existsSync(dir)) return results;
  
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
      results = results.concat(findAllFiles(filePath, extensions));
    } else if (stat.isFile() && extensions.some(ext => file.endsWith(ext))) {
      results.push(filePath);
    }
  }
  
  return results;
}

// Fix duplicate exports in a file
function fixDuplicateExports(content, filePath) {
  const lines = content.split('\n');
  const exportedComponents = new Set();
  const linesToRemove = new Set();
  
  // First pass: identify all export const/let/var declarations
  lines.forEach((line, index) => {
    const exportConstMatch = line.match(/^export\s+(const|let|var)\s+(\w+)/);
    if (exportConstMatch) {
      const componentName = exportConstMatch[2];
      exportedComponents.add(componentName);
    }
  });
  
  // Second pass: mark duplicate export { ComponentName } lines for removal
  lines.forEach((line, index) => {
    const exportBracesMatch = line.match(/^export\s*\{\s*(\w+)\s*\};?$/);
    if (exportBracesMatch) {
      const componentName = exportBracesMatch[1];
      if (exportedComponents.has(componentName)) {
        linesToRemove.add(index);
      }
    }
  });
  
  // Remove the duplicate lines
  const fixedLines = lines.filter((line, index) => !linesToRemove.has(index));
  
  return {
    content: fixedLines.join('\n'),
    removedCount: linesToRemove.size
  };
}

// Main processing
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to check\n`);

let totalFixed = 0;
let totalDuplicatesRemoved = 0;

allFiles.forEach((filePath, index) => {
  try {
    const originalContent = fs.readFileSync(filePath, 'utf8');
    const { content: fixedContent, removedCount } = fixDuplicateExports(originalContent, filePath);
    
    if (removedCount > 0) {
      fs.writeFileSync(filePath, fixedContent);
      totalFixed++;
      totalDuplicatesRemoved += removedCount;
      
      const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
      console.log(`✅ Fixed: ${relativePath} (removed ${removedCount} duplicate exports)`);
    }

  } catch (error) {
    const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
    console.log(`❌ Error fixing ${relativePath}: ${error.message}`);
  }
});

console.log('\n' + '='.repeat(60));
console.log(`🎉 DUPLICATE EXPORT FIXING COMPLETE!`);
console.log(`✅ Files fixed: ${totalFixed}`);
console.log(`🗑️  Duplicate exports removed: ${totalDuplicatesRemoved}`);
console.log('='.repeat(60));

if (totalFixed > 0) {
  console.log('\n🚀 ALL DUPLICATE EXPORT ISSUES RESOLVED!');
  console.log('🎯 Ready to build!');
} else {
  console.log('\n✨ No duplicate export issues found!');
}
