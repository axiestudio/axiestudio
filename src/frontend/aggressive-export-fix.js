const fs = require('fs');
const path = require('path');

console.log('🔧 AGGRESSIVE EXPORT FIXING - ADDING ALL MISSING NAMED EXPORTS...\n');

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

// Add missing named exports
function addMissingNamedExports(content, filePath) {
  const lines = content.split('\n');
  const exportedNames = new Set();
  const namedExportsToAdd = [];
  
  // First pass: find all export const/let/var declarations
  lines.forEach(line => {
    const exportConstMatch = line.trim().match(/^export\s+(const|let|var)\s+(\w+)/);
    if (exportConstMatch) {
      exportedNames.add(exportConstMatch[2]);
    }
  });
  
  // Second pass: find export default ComponentName and check if named export exists
  lines.forEach(line => {
    const exportDefaultMatch = line.trim().match(/^export default (\w+);?$/);
    if (exportDefaultMatch) {
      const componentName = exportDefaultMatch[1];
      
      // Check if we already have a named export for this component
      const hasNamedExport = content.includes(`export { ${componentName} }`);
      const hasExportConst = exportedNames.has(componentName);
      
      if (!hasNamedExport && !hasExportConst) {
        namedExportsToAdd.push(componentName);
      }
    }
  });
  
  // Add missing named exports
  if (namedExportsToAdd.length > 0) {
    let fixedContent = content;
    
    namedExportsToAdd.forEach(componentName => {
      fixedContent += `\nexport { ${componentName} };`;
    });
    
    return {
      content: fixedContent,
      added: namedExportsToAdd
    };
  }
  
  return {
    content,
    added: []
  };
}

// Main processing
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to process\n`);

let totalFilesFixed = 0;
let totalExportsAdded = 0;

console.log('🔧 Adding missing named exports...\n');

allFiles.forEach((filePath, index) => {
  try {
    const originalContent = fs.readFileSync(filePath, 'utf8');
    const result = addMissingNamedExports(originalContent, filePath);
    
    if (result.added.length > 0) {
      fs.writeFileSync(filePath, result.content);
      totalFilesFixed++;
      totalExportsAdded += result.added.length;
      
      const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
      console.log(`✅ ${relativePath}: Added exports for [${result.added.join(', ')}]`);
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
console.log(`🎉 AGGRESSIVE EXPORT FIXING COMPLETE!`);
console.log(`✅ Files fixed: ${totalFilesFixed}`);
console.log(`📦 Named exports added: ${totalExportsAdded}`);
console.log('='.repeat(80));

if (totalFilesFixed > 0) {
  console.log('\n🚀 ALL MISSING NAMED EXPORTS ADDED!');
  console.log('🎯 Ready to build!');
} else {
  console.log('\n✨ No missing named exports found!');
}
