const fs = require('fs');
const path = require('path');

// Find all modal files and fix them
const modalFiles = [
  'src/modals/shareModal/index.tsx',
  'src/modals/exportModal/index.tsx',
  'src/modals/apiModal/index.tsx',
  'src/modals/editNodeModal/index.tsx',
  'src/modals/toolsModal/index.tsx',
];

console.log('🔥 FIXING ALL MODAL FILES...');

modalFiles.forEach(filePath => {
  try {
    if (!fs.existsSync(filePath)) {
      console.log(`⚠️ File not found: ${filePath}`);
      return;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;

    // Fix the broken pattern: "export default function; export { function as ComponentName }; ComponentName({"
    const brokenPattern = /export default function;\s*export \{ function as (\w+) \};\s*(\w+)\(/;
    const match = content.match(brokenPattern);
    
    if (match) {
      const componentName = match[1];
      const functionName = match[2];
      
      // Replace with proper function declaration
      content = content.replace(
        brokenPattern,
        `function ${functionName}(`
      );
      
      // Add proper exports at the end
      content += `\n\nexport default ${functionName};\nexport { ${functionName} as ${componentName} };`;
      
      console.log(`✅ Fixed ${filePath} -> ${componentName}`);
    } else {
      // Check for other broken patterns
      const altPattern = /export default function;\s*export \{ function as (\w+) \};\s*/;
      const altMatch = content.match(altPattern);
      
      if (altMatch) {
        const componentName = altMatch[1];
        
        // Find the next function declaration
        const functionPattern = /(\w+)\s*\(/;
        const funcMatch = content.substring(content.indexOf(altMatch[0]) + altMatch[0].length).match(functionPattern);
        
        if (funcMatch) {
          const functionName = funcMatch[1];
          
          // Replace the broken export
          content = content.replace(altPattern, `function ${functionName}(`);
          
          // Add proper exports at the end
          content += `\n\nexport default ${functionName};\nexport { ${functionName} as ${componentName} };`;
          
          console.log(`✅ Fixed alt pattern ${filePath} -> ${componentName}`);
        }
      } else {
        console.log(`⚠️ No broken pattern found in ${filePath}`);
      }
    }

    // Write the fixed content
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content);
    }

  } catch (error) {
    console.log(`❌ Error fixing ${filePath}: ${error.message}`);
  }
});

console.log('🎉 FINISHED FIXING ALL MODALS!');
