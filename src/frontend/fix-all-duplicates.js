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
  const exportedNames = new Map(); // name -> {type, line, isFunction}
  const linesToRemove = new Set();
  let hasChanges = false;
  
  // First pass: catalog all exports
  lines.forEach((line, index) => {
    const trimmedLine = line.trim();
    
    // Check for export function ComponentName
    const exportFunctionMatch = trimmedLine.match(/^export\s+function\s+(\w+)/);
    if (exportFunctionMatch) {
      const componentName = exportFunctionMatch[1];
      exportedNames.set(componentName, {
        type: 'function',
        line: index + 1,
        isFunction: true
      });
    }
    
    // Check for export const ComponentName
    const exportConstMatch = trimmedLine.match(/^export\s+(const|let|var)\s+(\w+)/);
    if (exportConstMatch) {
      const componentName = exportConstMatch[2];
      exportedNames.set(componentName, {
        type: 'const',
        line: index + 1,
        isFunction: false
      });
    }
    
    // Check for export { ComponentName } or export { ComponentName as ComponentName }
    const exportBracesMatch = trimmedLine.match(/^export\s*\{\s*(\w+)(?:\s+as\s+\w+)?\s*\};?$/);
    if (exportBracesMatch) {
      const componentName = exportBracesMatch[1];

      // If we already have this component exported as function or const, remove this line
      if (exportedNames.has(componentName)) {
        linesToRemove.add(index);
        hasChanges = true;
      } else {
        // Track this export to catch future duplicates
        exportedNames.set(componentName, {
          type: 'braces',
          line: index + 1,
          isFunction: false
        });
      }
    }
  });
  
  if (hasChanges) {
    // Remove duplicate lines
    const fixedLines = lines.filter((line, index) => !linesToRemove.has(index));
    return {
      content: fixedLines.join('\n'),
      removedCount: linesToRemove.size,
      removedComponents: Array.from(linesToRemove).map(lineIndex => {
        const line = lines[lineIndex].trim();
        const match = line.match(/export\s*\{\s*(\w+)\s*\}/);
        return match ? match[1] : 'unknown';
      })
    };
  }
  
  return {
    content,
    removedCount: 0,
    removedComponents: []
  };
}

// Main processing
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to check\n`);

let totalFilesFixed = 0;
let totalDuplicatesRemoved = 0;

console.log('🔍 Checking for duplicate exports...\n');

allFiles.forEach((filePath, index) => {
  try {
    const originalContent = fs.readFileSync(filePath, 'utf8');
    const result = fixDuplicateExports(originalContent, filePath);
    
    if (result.removedCount > 0) {
      fs.writeFileSync(filePath, result.content);
      totalFilesFixed++;
      totalDuplicatesRemoved += result.removedCount;
      
      const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
      console.log(`✅ ${relativePath}: Removed ${result.removedCount} duplicate exports [${result.removedComponents.join(', ')}]`);
    }

    // Progress indicator
    if ((index + 1) % 100 === 0) {
      console.log(`📊 Processed ${index + 1}/${allFiles.length} files...`);
    }

  } catch (error) {
    const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
    console.log(`❌ Error processing ${relativePath}: ${error.message}`);
  }
});

console.log('\n' + '='.repeat(80));
console.log(`🎉 DUPLICATE EXPORT FIXING COMPLETE!`);
console.log(`✅ Files fixed: ${totalFilesFixed}`);
console.log(`🗑️  Duplicate exports removed: ${totalDuplicatesRemoved}`);
console.log('='.repeat(80));

if (totalFilesFixed > 0) {
  console.log('\n🚀 ALL DUPLICATE EXPORT ISSUES RESOLVED!');
  console.log('🎯 Ready to build!');
} else {
  console.log('\n✨ No duplicate export issues found!');
}
