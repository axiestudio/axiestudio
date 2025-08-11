const fs = require('fs');
const path = require('path');

console.log('🔥 FIXING REMAINING 458 CONST COMPONENT EXPORT ISSUES...\n');

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

// Function to add named export for existing default exports
function addNamedExport(content, filePath) {
  // Updated regex to handle both with and without semicolon
  const exportDefaultRegex = /export default (\w+);?$/gm;
  const matches = [...content.matchAll(exportDefaultRegex)];

  if (matches.length === 0) return content;

  let newContent = content;
  let hasChanges = false;

  matches.forEach(match => {
    const componentName = match[1];
    const fullMatch = match[0];

    // Check if named export already exists
    if (!newContent.includes(`export { ${componentName} }`)) {
      // Replace the default export line with both exports
      newContent = newContent.replace(
        fullMatch,
        `${fullMatch}\nexport { ${componentName} };`
      );
      hasChanges = true;
    }
  });

  return hasChanges ? newContent : content;
}

// Main processing
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to check\n`);

let totalFixed = 0;
let totalErrors = 0;
let filesWithIssues = 0;

console.log('🔍 Processing files for missing named exports...\n');

allFiles.forEach((filePath, index) => {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;

    // Check if file has export default but no named export
    const hasExportDefault = /export default \w+;?$/.test(content);
    const hasNamedExport = /export \{ \w+ \}/.test(content);
    
    if (hasExportDefault && !hasNamedExport) {
      filesWithIssues++;
      
      // Add named exports for existing default exports
      content = addNamedExport(content, filePath);

      // Write the fixed content
      if (content !== originalContent) {
        fs.writeFileSync(filePath, content);
        totalFixed++;
        
        const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
        console.log(`✅ Fixed: ${relativePath}`);
      }
    }

    // Progress indicator
    if ((index + 1) % 100 === 0) {
      console.log(`📊 Processed ${index + 1}/${allFiles.length} files...`);
    }

  } catch (error) {
    totalErrors++;
    const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
    console.log(`❌ Error fixing ${relativePath}: ${error.message}`);
  }
});

console.log('\n' + '='.repeat(80));
console.log(`🎉 FINAL EXPORT FIXING COMPLETE!`);
console.log(`📁 Total files scanned: ${allFiles.length}`);
console.log(`🔍 Files with missing named exports: ${filesWithIssues}`);
console.log(`✅ Files fixed: ${totalFixed}`);
console.log(`❌ Errors: ${totalErrors}`);
console.log('='.repeat(80));

if (totalFixed > 0) {
  console.log('\n🚀 ALL EXPORT ISSUES RESOLVED! Ready to build!');
} else {
  console.log('\n✨ No export issues found or all were already fixed!');
}
