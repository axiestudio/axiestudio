const fs = require('fs');
const path = require('path');

console.log('🔍 FINDING DUPLICATE EXPORT ISSUES...\n');

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

// Check for duplicate exports
function checkDuplicateExports(content, filePath) {
  const lines = content.split('\n');
  const exports = new Map();
  const issues = [];
  
  lines.forEach((line, index) => {
    // Check for export const/let/var ComponentName
    const exportConstMatch = line.match(/^export\s+(const|let|var)\s+(\w+)/);
    if (exportConstMatch) {
      const componentName = exportConstMatch[2];
      if (exports.has(componentName)) {
        issues.push({
          type: 'duplicate_export_const',
          componentName,
          line: index + 1,
          content: line.trim(),
          previousLine: exports.get(componentName)
        });
      } else {
        exports.set(componentName, index + 1);
      }
    }
    
    // Check for export { ComponentName }
    const exportBracesMatch = line.match(/^export\s*\{\s*(\w+)\s*\}/);
    if (exportBracesMatch) {
      const componentName = exportBracesMatch[1];
      if (exports.has(componentName)) {
        issues.push({
          type: 'duplicate_export_braces',
          componentName,
          line: index + 1,
          content: line.trim(),
          previousLine: exports.get(componentName)
        });
      } else {
        exports.set(componentName, index + 1);
      }
    }
  });
  
  return issues;
}

// Main processing
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to check\n`);

let totalIssues = 0;
const filesWithIssues = [];

allFiles.forEach((filePath, index) => {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const issues = checkDuplicateExports(content, filePath);
    
    if (issues.length > 0) {
      totalIssues += issues.length;
      const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
      filesWithIssues.push({
        file: relativePath,
        issues
      });
    }

  } catch (error) {
    // Skip files that can't be read
  }
});

console.log('📊 DUPLICATE EXPORT ANALYSIS:');
console.log('='.repeat(60));

if (totalIssues === 0) {
  console.log('🎉 NO DUPLICATE EXPORT ISSUES FOUND!');
  console.log('🚀 Ready to build!');
} else {
  console.log(`❌ Found ${totalIssues} duplicate export issues in ${filesWithIssues.length} files:`);
  
  filesWithIssues.forEach(({ file, issues }) => {
    console.log(`\n📄 ${file}:`);
    issues.forEach(issue => {
      console.log(`  ❌ Line ${issue.line}: ${issue.content}`);
      console.log(`     Conflicts with line ${issue.previousLine}`);
      console.log(`     Component: ${issue.componentName}`);
    });
  });
  
  console.log('\n🛠️  FIXES NEEDED:');
  console.log('- Remove duplicate export { ComponentName } lines');
  console.log('- Keep only the export const ComponentName declarations');
}

console.log('='.repeat(60));
