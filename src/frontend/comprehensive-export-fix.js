const fs = require('fs');
const path = require('path');

console.log('🔧 COMPREHENSIVE EXPORT ISSUE FIXING...\n');

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

// Comprehensive export analysis and fixing
function analyzeAndFixExports(content, filePath) {
  const lines = content.split('\n');
  const issues = [];
  const fixes = [];
  
  // Track all exports
  const exportedNames = new Map(); // name -> {type, line, declaration}
  const duplicateExportLines = new Set();
  
  lines.forEach((line, index) => {
    const lineNum = index + 1;
    const trimmedLine = line.trim();
    
    // Check for export const/let/var ComponentName
    const exportConstMatch = trimmedLine.match(/^export\s+(const|let|var)\s+(\w+)/);
    if (exportConstMatch) {
      const componentName = exportConstMatch[2];
      if (exportedNames.has(componentName)) {
        issues.push({
          type: 'duplicate_export_const',
          line: lineNum,
          component: componentName,
          content: trimmedLine
        });
      } else {
        exportedNames.set(componentName, {
          type: 'const',
          line: lineNum,
          declaration: trimmedLine
        });
      }
    }
    
    // Check for export { ComponentName }
    const exportBracesMatch = trimmedLine.match(/^export\s*\{\s*(\w+)\s*\};?$/);
    if (exportBracesMatch) {
      const componentName = exportBracesMatch[1];
      if (exportedNames.has(componentName)) {
        // This is a duplicate - mark for removal
        duplicateExportLines.add(index);
        issues.push({
          type: 'duplicate_export_braces',
          line: lineNum,
          component: componentName,
          content: trimmedLine,
          action: 'remove'
        });
      } else {
        exportedNames.set(componentName, {
          type: 'braces',
          line: lineNum,
          declaration: trimmedLine
        });
      }
    }
    
    // Check for export default ComponentName
    const exportDefaultMatch = trimmedLine.match(/^export default (\w+);?$/);
    if (exportDefaultMatch) {
      const componentName = exportDefaultMatch[1];
      
      // Check if we need to add a named export
      if (!exportedNames.has(componentName)) {
        issues.push({
          type: 'missing_named_export',
          line: lineNum,
          component: componentName,
          content: trimmedLine,
          action: 'add_named_export'
        });
      }
    }
  });
  
  // Apply fixes
  let fixedContent = content;
  
  // Remove duplicate export { ComponentName } lines
  if (duplicateExportLines.size > 0) {
    const fixedLines = lines.filter((line, index) => !duplicateExportLines.has(index));
    fixedContent = fixedLines.join('\n');
    fixes.push(`Removed ${duplicateExportLines.size} duplicate export lines`);
  }
  
  // Add missing named exports
  const missingNamedExports = issues.filter(issue => issue.action === 'add_named_export');
  if (missingNamedExports.length > 0) {
    missingNamedExports.forEach(issue => {
      if (!fixedContent.includes(`export { ${issue.component} }`)) {
        fixedContent += `\nexport { ${issue.component} };`;
        fixes.push(`Added named export for ${issue.component}`);
      }
    });
  }
  
  return {
    hasIssues: issues.length > 0,
    issues,
    fixes,
    fixedContent: fixedContent !== content ? fixedContent : null
  };
}

// Main processing
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to analyze\n`);

let totalFilesFixed = 0;
let totalIssuesFound = 0;
let totalFixesApplied = 0;

console.log('🔍 Analyzing and fixing export issues...\n');

allFiles.forEach((filePath, index) => {
  try {
    const originalContent = fs.readFileSync(filePath, 'utf8');
    const analysis = analyzeAndFixExports(originalContent, filePath);
    
    if (analysis.hasIssues) {
      totalIssuesFound += analysis.issues.length;
      
      const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
      console.log(`📄 ${relativePath}:`);
      
      analysis.issues.forEach(issue => {
        console.log(`  ${issue.type === 'duplicate_export_braces' ? '🗑️' : '⚠️'} Line ${issue.line}: ${issue.content}`);
      });
      
      if (analysis.fixedContent) {
        fs.writeFileSync(filePath, analysis.fixedContent);
        totalFilesFixed++;
        totalFixesApplied += analysis.fixes.length;
        
        console.log(`  ✅ Fixed: ${analysis.fixes.join(', ')}`);
      }
      
      console.log('');
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
console.log(`🎉 COMPREHENSIVE EXPORT FIXING COMPLETE!`);
console.log(`📊 Total issues found: ${totalIssuesFound}`);
console.log(`✅ Files fixed: ${totalFilesFixed}`);
console.log(`🔧 Total fixes applied: ${totalFixesApplied}`);
console.log('='.repeat(80));

if (totalFilesFixed > 0) {
  console.log('\n🚀 ALL EXPORT ISSUES SHOULD BE RESOLVED!');
  console.log('🎯 Ready to attempt build!');
} else {
  console.log('\n✨ No export issues found that needed fixing!');
}
