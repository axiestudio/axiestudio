const fs = require('fs');
const path = require('path');

console.log('🔥 FIXING ALL 458 EXPORT ISSUES AUTOMATICALLY...\n');

// Function to extract component name from file path
function getComponentNameFromPath(filePath) {
  const fileName = path.basename(filePath, path.extname(filePath));
  if (fileName === 'index') {
    const parentDir = path.basename(path.dirname(filePath));
    return parentDir.charAt(0).toUpperCase() + parentDir.slice(1);
  }
  return fileName.charAt(0).toUpperCase() + fileName.slice(1);
}

// Function to fix export default function pattern
function fixExportDefaultFunction(content, filePath) {
  const exportDefaultFunctionRegex = /export default function (\w+)/g;
  const matches = [...content.matchAll(exportDefaultFunctionRegex)];
  
  if (matches.length === 0) return content;
  
  let newContent = content;
  
  matches.forEach(match => {
    const functionName = match[1];
    
    // Replace export default function with just function
    newContent = newContent.replace(
      `export default function ${functionName}`,
      `function ${functionName}`
    );
    
    // Add exports at the end if not already there
    if (!newContent.includes(`export default ${functionName}`)) {
      newContent += `\n\nexport default ${functionName};\nexport { ${functionName} };`;
    }
  });
  
  return newContent;
}

// Function to add named export for existing default exports
function addNamedExport(content, filePath) {
  const exportDefaultRegex = /export default (\w+);$/gm;
  const matches = [...content.matchAll(exportDefaultRegex)];
  
  if (matches.length === 0) return content;
  
  let newContent = content;
  
  matches.forEach(match => {
    const componentName = match[1];
    const fullMatch = match[0];
    
    // Check if named export already exists
    if (!newContent.includes(`export { ${componentName} }`)) {
      // Replace the default export line with both exports
      newContent = newContent.replace(
        fullMatch,
        `${fullMatch}\nexport { ${componentName} };`
      );
    }
  });
  
  return newContent;
}

// List of files to fix (from our analysis)
const filesToFix = [
  // Export default function files (138 files)
  'alerts/alertDropDown/components/singleAlertComponent/index.tsx',
  'alerts/displayArea/index.tsx',
  'App.tsx',
  'components/common/crashErrorComponent/index.tsx',
  'components/common/fetchErrorComponent/index.tsx',
  'components/common/horizontalScrollFadeComponent/index.tsx',
  'components/common/ImageViewer/index.tsx',
  'components/common/loadingComponent/index.tsx',
  'components/common/numberReader/index.tsx',
  'components/common/objectRender/index.tsx',
  'components/common/pageLayout/index.tsx',
  'components/common/paginatorComponent/index.tsx',
  'components/common/storeCardComponent/index.tsx',
  'components/common/stringReaderComponent/index.tsx',
  'components/common/timeoutErrorComponent/index.tsx',
  'components/core/appHeaderComponent/index.tsx',
  'components/core/cardComponent/components/dragCardComponent/index.tsx',
  'components/core/cardsWrapComponent/index.tsx',
  'components/core/chatComponents/DurationDisplay.tsx',
  'components/core/codeTabsComponent/index.tsx',
  'components/core/dateReaderComponent/index.tsx',
  'components/core/dropdownComponent/index.tsx',
  'components/core/flowSettingsComponent/index.tsx',
  'components/core/flowToolbarComponent/components/deploy-dropdown.tsx',
  'components/core/flowToolbarComponent/components/flow-toolbar-options.tsx',
  'components/core/GlobalVariableModal/GlobalVariableModal.tsx',
  'components/core/GlobalVariableModal/utils/sort-by-name.tsx',
  'components/core/parameterRenderComponent/components/dictComponent/index.tsx',
  'components/core/parameterRenderComponent/components/floatComponent/index.tsx',
  'components/core/parameterRenderComponent/components/inputFileComponent/index.tsx',
  'components/core/parameterRenderComponent/components/inputListComponent/index.tsx',
  'components/core/parameterRenderComponent/components/intComponent/index.tsx',
  'components/core/parameterRenderComponent/components/linkComponent/index.tsx',
  'components/core/parameterRenderComponent/components/multiselectComponent/index.tsx',
  'components/core/parameterRenderComponent/components/queryComponent/index.tsx',
  'components/core/parameterRenderComponent/components/tableComponent/components/tableAutoCellRender/index.tsx',
  'components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellEditor/index.tsx',
  'components/core/parameterRenderComponent/components/ToolsComponent/index.tsx',
  'components/core/pdfViewer/Error/index.tsx',
  'components/core/pdfViewer/index.tsx',
  'components/core/pdfViewer/noData/index.tsx',
  'components/ui/checkmark.tsx',
  'components/ui/xmark.tsx',
  'contexts/index.tsx',
  'customization/components/custom-input-file.tsx',
  'customization/custom-App.tsx',
  'CustomNodes/GenericNode/components/HandleTooltipComponent/index.tsx',
  'CustomNodes/GenericNode/components/NodeDescription/index.tsx',
  'CustomNodes/GenericNode/components/NodeInputField/index.tsx',
  'CustomNodes/GenericNode/components/NodeInputInfo/index.tsx',
  'CustomNodes/GenericNode/components/NodeName/index.tsx',
  'CustomNodes/GenericNode/components/NodeOutputParameter/NodeOutputs.tsx',
  'CustomNodes/GenericNode/components/NodeStatus/index.tsx',
  'CustomNodes/GenericNode/components/NodeUpdateComponent/index.tsx',
  'CustomNodes/GenericNode/components/OutputComponent/index.tsx',
  'CustomNodes/GenericNode/components/outputModal/components/switchOutputView/components/index.tsx',
  'CustomNodes/GenericNode/components/outputModal/index.tsx',
  'CustomNodes/utils/get-field-title.tsx',
  'icons/Mem0/SvgMem.jsx',
  'icons/Streamlit/SvgStreamlit.jsx',
  'modals/addMcpServerModal/index.tsx',
  'modals/apiModal/codeTabs/code-tabs.tsx',
  'modals/apiModal/utils/get-widget-code.tsx',
  'modals/deleteConfirmationModal/index.tsx',
  'modals/dictAreaModal/index.tsx',
  'modals/EmbedModal/embed-modal.tsx',
  'modals/fileManagerModal/components/dragFilesComponent/index.tsx',
  'modals/fileManagerModal/components/filesContextMenuComponent/index.tsx',
  'modals/fileManagerModal/components/filesRendererComponent/index.tsx',
  'modals/fileManagerModal/components/importButtonComponent/index.tsx',
  'modals/fileManagerModal/components/recentFilesComponent/index.tsx',
  'modals/fileManagerModal/index.tsx',
  'modals/flowLogsModal/index.tsx',
  'modals/flowSettingsModal/index.tsx',
  'modals/IOModal/components/chatView/chatInput/chat-input.tsx',
  'modals/IOModal/components/chatView/chatMessage/chat-message.tsx',
  'modals/IOModal/components/chatView/chatMessage/components/chat-logo-icon.tsx',
  'modals/IOModal/components/chatView/chatMessage/components/edit-message-field.tsx',
  'modals/IOModal/components/chatView/chatMessage/components/file-card-wrapper.tsx',
  'modals/IOModal/components/chatView/components/chat-view.tsx',
  'modals/IOModal/components/chatView/fileComponent/components/download-button.tsx',
  'modals/IOModal/components/chatView/fileComponent/components/file-card.tsx',
  'modals/IOModal/components/chatView/fileComponent/components/file-preview.tsx',
  'modals/IOModal/components/chatView/fileComponent/utils/get-classes.tsx',
  'modals/IOModal/components/flow-running-squeleton.tsx',
  'modals/IOModal/components/IOFieldView/components/csv-selected.tsx',
  'modals/IOModal/components/IOFieldView/components/file-input.tsx',
  'modals/IOModal/components/IOFieldView/components/json-input.tsx',
  'modals/IOModal/components/IOFieldView/components/session-selector.tsx',
  'modals/IOModal/components/IOFieldView/io-field-view.tsx',
  'modals/IOModal/components/session-view.tsx',
  'modals/IOModal/playground-modal.tsx',
  'modals/promptModal/index.tsx',
  'modals/promptModal/utils/var-highlight-html.tsx',
  'modals/queryModal/index.tsx',
  'modals/secretKeyModal/index.tsx',
  'modals/shareModal/utils/get-tags-ids.tsx',
  'modals/templatesModal/components/GetStartedComponent/index.tsx',
  'modals/templatesModal/components/TemplateCardComponent/index.tsx',
  'modals/templatesModal/components/TemplateContentComponent/index.tsx',
  'modals/templatesModal/components/TemplateGetStartedCardComponent/index.tsx',
  'modals/textAreaModal/index.tsx',
  'modals/textModal/index.tsx',
  'modals/toolsModal/components/toolsTable/index.tsx',
  'modals/updateComponentModal/index.tsx',
  'modals/userManagementModal/index.tsx',
  'pages/AdminPage/index.tsx',
  'pages/AdminPage/LoginPage/index.tsx',
  'pages/DeleteAccountPage/index.tsx',
  'pages/FlowPage/components/flowBuildingComponent/index.tsx',
  'pages/FlowPage/components/flowSidebarComponent/helpers/sensitive-sort.tsx',
  'pages/FlowPage/components/nodeToolbarComponent/hooks/use-shortcuts.ts',
  'pages/FlowPage/components/nodeToolbarComponent/shortcutDisplay/index.tsx',
  'pages/FlowPage/components/nodeToolbarComponent/toolbarSelectItem/index.tsx',
  'pages/FlowPage/components/PageComponent/components/helper-lines.tsx',
  'pages/FlowPage/components/PageComponent/index.tsx',
  'pages/FlowPage/components/PageComponent/utils/get-random-name.tsx',
  'pages/FlowPage/components/SelectionMenuComponent/index.tsx',
  'pages/FlowPage/components/UpdateAllComponents/index.tsx',
  'pages/FlowPage/index.tsx',
  'pages/LoginPage/index.tsx',
  'pages/MainPage/pages/filesPage/components/dragWrapComponent/index.tsx',
  'pages/MainPage/pages/main-page.tsx',
  'pages/Playground/index.tsx',
  'pages/SettingsPage/index.tsx',
  'pages/SettingsPage/pages/ApiKeysPage/index.tsx',
  'pages/SettingsPage/pages/GeneralPage/components/ProfilePictureForm/components/profilePictureChooserComponent/index.tsx',
  'pages/SettingsPage/pages/GlobalVariablesPage/index.tsx',
  'pages/SettingsPage/pages/MCPServersPage/index.tsx',
  'pages/SettingsPage/pages/messagesPage/index.tsx',
  'pages/SettingsPage/pages/ShortcutsPage/CellRenderWrapper/index.tsx',
  'pages/SettingsPage/pages/ShortcutsPage/EditShortcutButton/index.tsx',
  'pages/SettingsPage/pages/ShortcutsPage/index.tsx',
  'pages/SignUpPage/index.tsx',
  'pages/StorePage/index.tsx',
  'pages/ViewPage/index.tsx',
  'stores/globalVariablesStore/utils/get-unavailable-fields.tsx',
  'utils/storeUtils.ts'
];

// Process files in batches to avoid overwhelming the system
const BATCH_SIZE = 50;
let totalFixed = 0;
let totalErrors = 0;

for (let i = 0; i < filesToFix.length; i += BATCH_SIZE) {
  const batch = filesToFix.slice(i, i + BATCH_SIZE);
  
  console.log(`\n📦 Processing batch ${Math.floor(i/BATCH_SIZE) + 1}/${Math.ceil(filesToFix.length/BATCH_SIZE)} (${batch.length} files)...`);
  
  batch.forEach(filePath => {
    try {
      if (!fs.existsSync(filePath)) {
        console.log(`⚠️ File not found: ${filePath}`);
        return;
      }

      let content = fs.readFileSync(filePath, 'utf8');
      const originalContent = content;

      // Fix export default function pattern
      content = fixExportDefaultFunction(content, filePath);
      
      // Add named exports for existing default exports
      content = addNamedExport(content, filePath);

      // Write the fixed content
      if (content !== originalContent) {
        fs.writeFileSync(filePath, content);
        totalFixed++;
        console.log(`✅ Fixed: ${filePath}`);
      }

    } catch (error) {
      totalErrors++;
      console.log(`❌ Error fixing ${filePath}: ${error.message}`);
    }
  });
}

console.log('\n' + '='.repeat(80));
console.log(`🎉 BATCH PROCESSING COMPLETE!`);
console.log(`✅ Fixed: ${totalFixed} files`);
console.log(`❌ Errors: ${totalErrors} files`);
console.log(`📊 Total processed: ${filesToFix.length} files`);
console.log('='.repeat(80));
