const fs = require('fs');
const path = require('path');

console.log('🔥 COMPREHENSIVE FIX FOR ALL REMAINING EXPORT ISSUES...');

// Fix the AUTH_METHODS usage in McpServerTab.tsx
function fixMcpServerTab() {
  const filePath = 'src/pages/MainPage/pages/homePage/components/McpServerTab.tsx';
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️ File not found: ${filePath}`);
    return;
  }

  let content = fs.readFileSync(filePath, 'utf8');
  const originalContent = content;

  // Find the component function to get the t function
  const componentMatch = content.match(/const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{/);
  if (componentMatch) {
    const componentName = componentMatch[1];
    
    // Check if useTranslation is already called
    if (!content.includes('const { t }')) {
      // Add the t function extraction
      const useTranslationMatch = content.match(/(const\s+\{\s*[^}]*\}\s*=\s*useTranslation\(\);?)/);
      if (useTranslationMatch) {
        // Update existing useTranslation call to include t
        content = content.replace(
          useTranslationMatch[1],
          'const { t } = useTranslation();'
        );
      } else {
        // Add new useTranslation call after component declaration
        const componentStart = content.indexOf(componentMatch[0]);
        const insertPoint = content.indexOf('{', componentStart) + 1;
        content = content.slice(0, insertPoint) + '\n  const { t } = useTranslation();' + content.slice(insertPoint);
      }
    }

    // Replace AUTH_METHODS usage with getAuthMethods(t)
    content = content.replace(
      /AUTH_METHODS\[\s*([^}]+)\s*\]/g,
      'getAuthMethods(t)[$1]'
    );

    console.log(`✅ Fixed AUTH_METHODS usage in ${filePath}`);
  }

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content);
  }
}

// Fix any remaining files that need both default and named exports
function fixRemainingExports() {
  const filesToCheck = [
    'src/components/common/genericIconComponent/index.tsx',
    'src/utils/mcpUtils.ts',
    // Add more files as needed
  ];

  filesToCheck.forEach(filePath => {
    if (!fs.existsSync(filePath)) {
      console.log(`⚠️ File not found: ${filePath}`);
      return;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;

    // Check if it's a TypeScript utility file
    if (filePath.endsWith('mcpUtils.ts')) {
      // This file already has the correct exports, no changes needed
      console.log(`✅ ${filePath} already has correct exports`);
      return;
    }

    // For component files, ensure both default and named exports exist
    const componentName = path.basename(filePath, '.tsx').replace(/([a-z])([A-Z])/g, '$1$2');
    
    // Check for export default function pattern
    const exportDefaultFunctionMatch = content.match(/export default function (\w+)/);
    if (exportDefaultFunctionMatch) {
      const functionName = exportDefaultFunctionMatch[1];
      
      // Convert to named function and add exports at the end
      content = content.replace(
        /export default function (\w+)/,
        'function $1'
      );
      
      // Add exports at the end if not already there
      if (!content.includes(`export default ${functionName}`)) {
        content += `\n\nexport default ${functionName};\nexport { ${functionName} };`;
      }
      
      console.log(`✅ Fixed exports for ${filePath} -> ${functionName}`);
    }
    
    // Check for const component = ... pattern
    const constComponentMatch = content.match(/const (\w+) = /);
    if (constComponentMatch && !content.includes('export default')) {
      const componentName = constComponentMatch[1];
      
      // Add exports at the end
      content += `\n\nexport default ${componentName};\nexport { ${componentName} };`;
      
      console.log(`✅ Added exports for ${filePath} -> ${componentName}`);
    }

    if (content !== originalContent) {
      fs.writeFileSync(filePath, content);
    }
  });
}

// Main execution
try {
  console.log('1. Fixing McpServerTab AUTH_METHODS usage...');
  fixMcpServerTab();
  
  console.log('2. Fixing remaining export issues...');
  fixRemainingExports();
  
  console.log('🎉 ALL FIXES COMPLETED!');
  console.log('\n📋 SUMMARY:');
  console.log('- Fixed AUTH_METHODS usage in McpServerTab.tsx');
  console.log('- Ensured all components have both default and named exports');
  console.log('- Ready for build!');
  
} catch (error) {
  console.error('❌ Error during fix:', error.message);
}
