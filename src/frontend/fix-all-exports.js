const fs = require('fs');
const path = require('path');

// List of all components that need both default and named exports
const componentsToFix = [
  'src/CustomNodes/GenericNode/components/ListSelectionComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/codeAreaComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/connectionComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/promptComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/strRenderComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/TableNodeComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/sliderComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/tabComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/toggleShadComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/mcpComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/copyFieldAreaComponent/index.tsx',
  'src/components/core/codeTabsComponent/components/tweakComponent/index.tsx',
  'src/components/core/chatComponents/ContentDisplay.tsx',
  'src/modals/IOModal/index.tsx',
  'src/modals/shareModal/index.tsx',
  'src/modals/exportModal/index.tsx',
  'src/modals/apiModal/index.tsx',
  'src/modals/templatesModal/index.tsx',
  'src/modals/editNodeModal/index.tsx',
  'src/modals/toolsModal/index.tsx',
  'src/modals/GlobalVariableModal/GlobalVariableModal.tsx',
];

console.log('🔥 FIXING ALL EXPORT ISSUES AT ONCE...');

componentsToFix.forEach(filePath => {
  try {
    if (!fs.existsSync(filePath)) {
      console.log(`⚠️ File not found: ${filePath}`);
      return;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;

    // Extract component name from file path
    const fileName = path.basename(filePath, '.tsx');
    let componentName;
    
    if (fileName === 'index') {
      // Get component name from parent directory
      const parentDir = path.basename(path.dirname(filePath));
      componentName = parentDir;
    } else {
      componentName = fileName;
    }

    // Handle special cases
    const specialNames = {
      'ListSelectionComponent': 'ListSelectionComponent',
      'codeAreaComponent': 'CodeAreaComponent',
      'connectionComponent': 'ConnectionComponent',
      'promptComponent': 'PromptComponent',
      'strRenderComponent': 'StrRenderComponent',
      'TableNodeComponent': 'TableNodeComponent',
      'sliderComponent': 'SliderComponent',
      'tabComponent': 'TabComponent',
      'toggleShadComponent': 'ToggleShadComponent',
      'mcpComponent': 'McpComponent',
      'copyFieldAreaComponent': 'CopyFieldAreaComponent',
      'tweakComponent': 'TweakComponent',
      'ContentDisplay': 'ContentDisplay',
      'IOModal': 'IOModal',
      'shareModal': 'ShareModal',
      'exportModal': 'ExportModal',
      'apiModal': 'ApiModal',
      'templatesModal': 'TemplatesModal',
      'editNodeModal': 'EditNodeModal',
      'toolsModal': 'ToolsModal',
      'GlobalVariableModal': 'GlobalVariableModal',
    };

    const finalComponentName = specialNames[componentName] || componentName;

    // Check if it already has named export
    if (content.includes(`export { ${finalComponentName} }`)) {
      console.log(`✅ ${filePath} already has named export`);
      return;
    }

    // Find the export default line
    const exportDefaultRegex = /export default (\w+);?/;
    const match = content.match(exportDefaultRegex);
    
    if (match) {
      const exportedName = match[1];
      // Add named export after the default export
      content = content.replace(
        exportDefaultRegex,
        `export default ${exportedName};\nexport { ${exportedName} as ${finalComponentName} };`
      );
    } else {
      // Look for export default function pattern
      const functionExportRegex = /export default function (\w+)/;
      const functionMatch = content.match(functionExportRegex);
      
      if (functionMatch) {
        const functionName = functionMatch[1];
        // Change to named function and add exports at the end
        content = content.replace(
          functionExportRegex,
          `function ${functionName}`
        );
        
        // Add exports at the end
        content += `\n\nexport default ${functionName};\nexport { ${functionName} as ${finalComponentName} };`;
      } else {
        // Look for const component = ... pattern
        const constRegex = /const (\w+) = /;
        const constMatch = content.match(constRegex);
        
        if (constMatch) {
          const constName = constMatch[1];
          // Add exports at the end if not already there
          if (!content.includes(`export default ${constName}`)) {
            content += `\n\nexport default ${constName};\nexport { ${constName} as ${finalComponentName} };`;
          } else {
            // Just add named export
            content = content.replace(
              `export default ${constName};`,
              `export default ${constName};\nexport { ${constName} as ${finalComponentName} };`
            );
          }
        }
      }
    }

    // Only write if content changed
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed exports for ${filePath} -> ${finalComponentName}`);
    } else {
      console.log(`⚠️ Could not fix ${filePath}`);
    }

  } catch (error) {
    console.log(`❌ Error fixing ${filePath}: ${error.message}`);
  }
});

console.log('🎉 FINISHED FIXING ALL EXPORTS!');
