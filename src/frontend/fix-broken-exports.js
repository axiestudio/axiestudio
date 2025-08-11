const fs = require('fs');

// Fix files that got broken by the export script
const brokenFiles = [
  'src/components/core/parameterRenderComponent/components/toggleShadComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/mcpComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/copyFieldAreaComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/codeAreaComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/connectionComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/promptComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/strRenderComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/TableNodeComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/sliderComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/tabComponent/index.tsx',
];

console.log('🔥 FIXING BROKEN EXPORT FILES...');

brokenFiles.forEach(filePath => {
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
      console.log(`⚠️ No broken pattern found in ${filePath}`);
    }

    // Write the fixed content
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content);
    }

  } catch (error) {
    console.log(`❌ Error fixing ${filePath}: ${error.message}`);
  }
});

console.log('🎉 FINISHED FIXING BROKEN EXPORTS!');
