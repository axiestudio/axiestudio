const fs = require('fs');
const path = require('path');

// Fix all remaining TypeScript errors efficiently
const fixes = [
  // Fix switchOutputView/index.tsx
  {
    file: 'src/CustomNodes/GenericNode/components/outputModal/components/switchOutputView/index.tsx',
    find: 'type: t("common.outputs") | "Logs";',
    replace: 'type: string;'
  },
  
  // Fix use-merge-refs.ts - add missing closing brace
  {
    file: 'src/CustomNodes/hooks/use-merge-refs.ts',
    find: /(\): ref is \(instance: T \| null\) => void \{[^}]*$)/s,
    replace: (match) => match + '\n}'
  },
  
  // Fix codeAreaModal/index.tsx
  {
    file: 'src/modals/codeAreaModal/index.tsx',
    find: 'import type ReactAce } from "react-ace/lib/ace";',
    replace: 'import type { ReactAce } from "react-ace/lib/ace";'
  },
  
  // Fix importButtonComponent/index.tsx
  {
    file: 'src/modals/fileManagerModal/components/importButtonComponent/index.tsx',
    find: 'variant = "large",: {',
    replace: 'variant = "large"'
  },
  
  // Fix voice-assistant utils.ts - add missing closing brace
  {
    file: 'src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/utils.ts',
    find: /export function base64ToFloat32Array\(base64String: string\): Float32Array \{[^}]*$/s,
    replace: (match) => match + '\n}'
  },
  
  // Fix content-view.tsx - move useTranslation hook
  {
    file: 'src/modals/IOModal/components/chatView/chatMessage/components/content-view.tsx',
    find: /\{\s*const \{ t \} = useTranslation\(\);\s*blocks: any;/,
    replace: '{ blocks: any;'
  },
  
  // Fix format-file-name.tsx - add missing closing brace
  {
    file: 'src/modals/IOModal/components/chatView/fileComponent/utils/format-file-name.tsx',
    find: /\): string \{[^}]*$/s,
    replace: (match) => match + '\n}'
  },
  
  // Fix tableModal/index.tsx
  {
    file: 'src/modals/tableModal/index.tsx',
    find: 'import TableComponent, { import { type TableComponentProps } from "@/components/core/parameterRenderComponent/components/tableComponent";',
    replace: 'import TableComponent, { type TableComponentProps } from "@/components/core/parameterRenderComponent/components/tableComponent";'
  },
  
  // Fix types/api/index.ts - remove useTranslation import and fix broken syntax
  {
    file: 'src/types/api/index.ts',
    find: 'import { useTranslation } from "react-i18next";',
    replace: ''
  },
  
  // Fix markdownUtils.ts - add missing closing brace
  {
    file: 'src/utils/markdownUtils.ts',
    find: /export const isMarkdownTable = \(text: string\): boolean => \{[^}]*$/s,
    replace: (match) => match + '\n}'
  },
  
  // Fix test file
  {
    file: 'tests/utils/await-bootstrap-test.ts',
    find: 'await addFlowToTestOnEmptyAxie Studio(page);',
    replace: 'await addFlowToTestOnEmptyAxieStudio(page);'
  }
];

console.log('🔥 RAPID BATCH FIX - Fixing all TypeScript errors...');

let fixedCount = 0;

fixes.forEach(({ file, find, replace }) => {
  try {
    const filePath = path.join('.', file);
    if (!fs.existsSync(filePath)) {
      console.log(`⚠️  File not found: ${file}`);
      return;
    }
    
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    if (typeof find === 'string') {
      if (content.includes(find)) {
        content = content.replace(find, replace);
        modified = true;
      }
    } else if (find instanceof RegExp) {
      if (find.test(content)) {
        content = content.replace(find, replace);
        modified = true;
      }
    }
    
    if (modified) {
      fs.writeFileSync(filePath, content);
      console.log(`✅ Fixed: ${file}`);
      fixedCount++;
    }
  } catch (error) {
    console.error(`❌ Error fixing ${file}: ${error.message}`);
  }
});

// Additional comprehensive fixes
console.log('\n🔧 Running additional comprehensive fixes...');

function walkAndFix(dir) {
  const files = fs.readdirSync(dir);
  let count = 0;
  
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && !file.includes('node_modules')) {
      count += walkAndFix(fullPath);
    } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
      try {
        let content = fs.readFileSync(fullPath, 'utf8');
        let modified = false;
        
        // Fix broken import statements
        const importFixes = [
          { regex: /import\s*{\s*import\s*{\s*([^}]+)\s*}\s*from/g, replacement: 'import { $1 } from' },
          { regex: /import\s*{\s*type\s*{\s*([^}]+)\s*}\s*from/g, replacement: 'import type { $1 } from' },
          { regex: /import\s*{\s*\*\s*as\s+([^}]+)\s*}\s*from/g, replacement: 'import * as $1 from' },
        ];
        
        importFixes.forEach(({ regex, replacement }) => {
          const oldContent = content;
          content = content.replace(regex, replacement);
          if (oldContent !== content) modified = true;
        });
        
        // Fix useTranslation hooks in wrong places
        if (content.includes('const { t } = useTranslation();')) {
          // Remove useTranslation from type definitions
          content = content.replace(/\{\s*const\s*{\s*t\s*}\s*=\s*useTranslation\(\);\s*([^}]+)\s*\}/g, '{ $1 }');
          modified = true;
        }
        
        if (modified) {
          fs.writeFileSync(fullPath, content);
          count++;
        }
      } catch (error) {
        // Skip files that can't be read
      }
    }
  });
  
  return count;
}

const additionalFixes = walkAndFix('./src');
console.log(`✅ Additional fixes applied to ${additionalFixes} files`);

console.log(`\n🎉 TOTAL FIXES: ${fixedCount + additionalFixes} files fixed!`);
console.log('🔧 Now attempting build...');

// Try to build
const { execSync } = require('child_process');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('🎉 BUILD SUCCESSFUL!');
  
  console.log('🔧 Copying to backend...');
  execSync('Remove-Item -Recurse -Force "..\\..\\src\\backend\\base\\axiestudio\\frontend\\*" -ErrorAction SilentlyContinue', { shell: 'powershell' });
  execSync('Copy-Item -Recurse -Force "build\\*" "..\\..\\src\\backend\\base\\axiestudio\\frontend\\"', { shell: 'powershell' });
  console.log('🎉 SUCCESS! Swedish translations deployed!');
  
} catch (error) {
  console.log('❌ Build still has errors. Running TypeScript check...');
  try {
    execSync('npx tsc --noEmit --pretty', { stdio: 'inherit' });
  } catch (tscError) {
    console.log('❌ TypeScript errors remain. Manual fixes needed.');
  }
}
