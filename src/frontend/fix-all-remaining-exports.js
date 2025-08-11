const fs = require('fs');

// List of ALL remaining components that need named exports
const componentsToFix = [
  'src/components/core/parameterRenderComponent/components/inputGlobalComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/dropdownComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/copyFieldAreaComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellEditor/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellRenderer/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellFilter/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellFloatingFilter/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellComparator/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellValueGetter/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellValueSetter/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellValueFormatter/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellValueParser/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellKeyCreator/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellClass/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellStyle/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellHeaderClass/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellHeaderStyle/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellTooltip/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellTooltipField/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellTooltipValueGetter/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellHeaderTooltip/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellRenderer/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellHeaderComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellHeaderComponentParams/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellFloatingFilterComponent/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellFloatingFilterComponentParams/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellFilterFramework/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellFilterParams/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellRendererFramework/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellRendererParams/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellEditorFramework/index.tsx',
  'src/components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellCellEditorParams/index.tsx',
];

console.log('🔥 FIXING ALL REMAINING COMPONENT EXPORTS...');

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

    // Convert to PascalCase
    const pascalCase = componentName.replace(/([a-z])([A-Z])/g, '$1$2')
      .replace(/^[a-z]/, c => c.toUpperCase())
      .replace(/Component$/, 'Component');

    // Check if it already has named export
    if (content.includes(`export { ${pascalCase} }`)) {
      console.log(`✅ ${filePath} already has named export`);
      return;
    }

    // Find export default pattern
    const exportDefaultRegex = /export default (\w+);?/;
    const match = content.match(exportDefaultRegex);
    
    if (match) {
      const exportedName = match[1];
      // Add named export after the default export
      content = content.replace(
        exportDefaultRegex,
        `export default ${exportedName};\nexport { ${exportedName} as ${pascalCase} };`
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
        content += `\n\nexport default ${functionName};\nexport { ${functionName} as ${pascalCase} };`;
      } else {
        console.log(`⚠️ No export pattern found in ${filePath}`);
        return;
      }
    }

    // Only write if content changed
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed exports for ${filePath} -> ${pascalCase}`);
    }

  } catch (error) {
    console.log(`❌ Error fixing ${filePath}: ${error.message}`);
  }
});

// Also fix the specific ones we know about
const specificFixes = [
  {
    file: 'src/components/core/parameterRenderComponent/components/inputGlobalComponent/index.tsx',
    name: 'InputGlobalComponent'
  },
  {
    file: 'src/components/core/parameterRenderComponent/components/dropdownComponent/index.tsx',
    name: 'DropdownComponent'
  }
];

specificFixes.forEach(({ file, name }) => {
  try {
    if (!fs.existsSync(file)) {
      console.log(`⚠️ File not found: ${file}`);
      return;
    }

    let content = fs.readFileSync(file, 'utf8');
    
    // Check if named export already exists
    if (content.includes(`export { ${name} }`)) {
      console.log(`✅ ${file} already has named export`);
      return;
    }

    // Find export default and add named export
    const exportDefaultRegex = /export default (\w+);?/;
    const match = content.match(exportDefaultRegex);
    
    if (match) {
      const exportedName = match[1];
      content = content.replace(
        exportDefaultRegex,
        `export default ${exportedName};\nexport { ${exportedName} as ${name} };`
      );
      
      fs.writeFileSync(file, content);
      console.log(`✅ Fixed specific export for ${file} -> ${name}`);
    } else {
      // Try function export pattern
      const functionExportRegex = /export default function (\w+)/;
      const functionMatch = content.match(functionExportRegex);
      
      if (functionMatch) {
        const functionName = functionMatch[1];
        content = content.replace(functionExportRegex, `function ${functionName}`);
        content += `\n\nexport default ${functionName};\nexport { ${functionName} as ${name} };`;
        
        fs.writeFileSync(file, content);
        console.log(`✅ Fixed function export for ${file} -> ${name}`);
      }
    }

  } catch (error) {
    console.log(`❌ Error fixing ${file}: ${error.message}`);
  }
});

console.log('🎉 FINISHED FIXING ALL REMAINING EXPORTS!');
