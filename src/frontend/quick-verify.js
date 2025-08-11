const fs = require('fs');
const path = require('path');

console.log('🔍 QUICK VERIFICATION OF ACTUAL EXPORT STATUS...\n');

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

// Check actual export status
function checkExportStatus(content, filePath) {
  const hasExportDefault = /^export default \w+;?$/m.test(content);
  const hasNamedExport = /^export \{ \w+ \};?$/m.test(content);
  
  return {
    hasExportDefault,
    hasNamedExport,
    needsFix: hasExportDefault && !hasNamedExport
  };
}

// Main verification
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to verify\n`);

let totalNeedingFix = 0;
let totalWithBothExports = 0;
let totalWithOnlyDefault = 0;
let sampleIssues = [];

allFiles.forEach((filePath, index) => {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const status = checkExportStatus(content, filePath);
    
    if (status.hasExportDefault && status.hasNamedExport) {
      totalWithBothExports++;
    } else if (status.hasExportDefault && !status.hasNamedExport) {
      totalWithOnlyDefault++;
      totalNeedingFix++;
      
      // Collect first 10 samples
      if (sampleIssues.length < 10) {
        const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
        sampleIssues.push(relativePath);
      }
    }

  } catch (error) {
    // Skip files that can't be read
  }
});

console.log('📊 VERIFICATION RESULTS:');
console.log('='.repeat(60));
console.log(`✅ Files with both default and named exports: ${totalWithBothExports}`);
console.log(`⚠️  Files with only default export: ${totalWithOnlyDefault}`);
console.log(`❌ Total files still needing fixes: ${totalNeedingFix}`);
console.log('='.repeat(60));

if (totalNeedingFix > 0) {
  console.log('\n🔍 SAMPLE FILES STILL NEEDING FIXES:');
  sampleIssues.forEach((file, i) => {
    console.log(`${i + 1}. ${file}`);
  });
  
  console.log('\n❌ BUILD WILL LIKELY FAIL - More fixes needed!');
  console.log('🛠️  Recommendation: Run additional fix script before building');
} else {
  console.log('\n🎉 ALL EXPORT ISSUES RESOLVED!');
  console.log('🚀 BUILD SHOULD SUCCEED!');
}
