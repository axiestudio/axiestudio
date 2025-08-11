const fs = require('fs');
const path = require('path');

console.log('🔍 COMPREHENSIVE ANALYSIS OF ALL EXPORT/IMPORT ISSUES...\n');

// Issues to check for
const issuePatterns = [
  {
    name: 'AUTH_METHODS usage',
    pattern: /AUTH_METHODS(?!\w)/g,
    description: 'Should use getAuthMethods(t) instead'
  },
  {
    name: 'AUTH_METHODS_ARRAY usage', 
    pattern: /AUTH_METHODS_ARRAY(?!\w)/g,
    description: 'Should use getAuthMethodsArray(t) instead'
  },
  {
    name: 'Missing named exports for components',
    pattern: /export default function (\w+)/g,
    description: 'Components need both default and named exports'
  },
  {
    name: 'Missing named exports for const components',
    pattern: /export default (\w+);$/gm,
    description: 'Need to add named export'
  },
  {
    name: 'Incorrect react-markdown import',
    pattern: /import \{ Markdown \} from "react-markdown"/g,
    description: 'Should be default import'
  },
  {
    name: 'Incorrect remark-gfm import',
    pattern: /import \{ remarkGfm \} from "remark-gfm"/g,
    description: 'Should be default import'
  }
];

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

// Analyze a single file for all issues
function analyzeFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const issues = [];
    
    issuePatterns.forEach(({ name, pattern, description }) => {
      const matches = [...content.matchAll(pattern)];
      if (matches.length > 0) {
        matches.forEach(match => {
          const lines = content.substring(0, match.index).split('\n');
          const lineNumber = lines.length;
          const lineContent = lines[lines.length - 1] + match[0];
          
          issues.push({
            type: name,
            description,
            lineNumber,
            lineContent: lineContent.trim(),
            match: match[0]
          });
        });
      }
    });
    
    return issues;
  } catch (error) {
    console.log(`❌ Error reading ${filePath}: ${error.message}`);
    return [];
  }
}

// Main analysis
console.log('📁 Finding all TypeScript/JavaScript files...');
const allFiles = findAllFiles('src');
console.log(`Found ${allFiles.length} files to analyze\n`);

let totalIssues = 0;
const fileIssues = {};

console.log('🔍 ANALYZING FILES FOR ISSUES...\n');

allFiles.forEach(filePath => {
  const issues = analyzeFile(filePath);
  if (issues.length > 0) {
    fileIssues[filePath] = issues;
    totalIssues += issues.length;
  }
});

// Report results
console.log('📊 ANALYSIS RESULTS:');
console.log('='.repeat(80));

if (totalIssues === 0) {
  console.log('🎉 NO ISSUES FOUND! The codebase looks clean.');
} else {
  console.log(`❌ Found ${totalIssues} issues across ${Object.keys(fileIssues).length} files:\n`);
  
  // Group issues by type
  const issuesByType = {};
  Object.entries(fileIssues).forEach(([filePath, issues]) => {
    issues.forEach(issue => {
      if (!issuesByType[issue.type]) {
        issuesByType[issue.type] = [];
      }
      issuesByType[issue.type].push({ filePath, ...issue });
    });
  });
  
  // Report by issue type
  Object.entries(issuesByType).forEach(([issueType, issues]) => {
    console.log(`\n🔴 ${issueType.toUpperCase()} (${issues.length} occurrences):`);
    console.log('-'.repeat(60));
    
    issues.forEach(({ filePath, lineNumber, lineContent, description }) => {
      const relativePath = filePath.replace(/\\/g, '/').replace('src/', '');
      console.log(`  📄 ${relativePath}:${lineNumber}`);
      console.log(`     ${lineContent}`);
      console.log(`     💡 ${description}\n`);
    });
  });
  
  // Summary of fixes needed
  console.log('\n🛠️  FIXES NEEDED:');
  console.log('='.repeat(80));
  
  if (issuesByType['AUTH_METHODS usage']) {
    console.log('1. Replace AUTH_METHODS with getAuthMethods(t)');
    console.log('   - Add useTranslation() hook if missing');
    console.log('   - Update import to use getAuthMethods');
  }
  
  if (issuesByType['AUTH_METHODS_ARRAY usage']) {
    console.log('2. Replace AUTH_METHODS_ARRAY with getAuthMethodsArray(t)');
    console.log('   - Add useTranslation() hook if missing');
    console.log('   - Update import to use getAuthMethodsArray');
  }
  
  if (issuesByType['Missing named exports for components']) {
    console.log('3. Add named exports for components');
    console.log('   - Change "export default function Name" to "function Name"');
    console.log('   - Add "export default Name; export { Name };" at end');
  }
  
  if (issuesByType['Missing named exports for const components']) {
    console.log('4. Add named exports for const components');
    console.log('   - Add "export { ComponentName };" after default export');
  }
  
  if (issuesByType['Incorrect react-markdown import']) {
    console.log('5. Fix react-markdown imports');
    console.log('   - Change to default import: import Markdown from "react-markdown"');
  }
  
  if (issuesByType['Incorrect remark-gfm import']) {
    console.log('6. Fix remark-gfm imports');
    console.log('   - Change to default import: import remarkGfm from "remark-gfm"');
  }
}

console.log('\n' + '='.repeat(80));
console.log(`✅ Analysis complete! ${totalIssues} issues found.`);
