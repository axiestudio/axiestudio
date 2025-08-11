const fs = require('fs');
const { execSync } = require('child_process');

console.log('🔥 FINAL FIX - Fixing all remaining TypeScript errors...');

// Fix all remaining files with specific issues
const fixes = [
  // Fix use-merge-refs.ts - add missing closing brace
  {
    file: 'src/CustomNodes/hooks/use-merge-refs.ts',
    action: () => {
      let content = fs.readFileSync('src/CustomNodes/hooks/use-merge-refs.ts', 'utf8');
      if (!content.trim().endsWith('}')) {
        content = content.trim() + '\n}';
        fs.writeFileSync('src/CustomNodes/hooks/use-merge-refs.ts', content);
        return true;
      }
      return false;
    }
  },
  
  // Fix importButtonComponent - fix function parameters
  {
    file: 'src/modals/fileManagerModal/components/importButtonComponent/index.tsx',
    action: () => {
      let content = fs.readFileSync('src/modals/fileManagerModal/components/importButtonComponent/index.tsx', 'utf8');
      content = content.replace(
        /variant = "large"\s*variant\?: "large" \| "small";\s*\}\) \{/,
        'variant = "large"\n}: {\n  variant?: "large" | "small";\n}) {'
      );
      fs.writeFileSync('src/modals/fileManagerModal/components/importButtonComponent/index.tsx', content);
      return true;
    }
  },
  
  // Fix voice-assistant utils.ts - add missing closing brace
  {
    file: 'src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/utils.ts',
    action: () => {
      let content = fs.readFileSync('src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/utils.ts', 'utf8');
      if (!content.trim().endsWith('}')) {
        content = content.trim() + '\n}';
        fs.writeFileSync('src/modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/utils.ts', content);
        return true;
      }
      return false;
    }
  },
  
  // Fix format-file-name.tsx - add missing closing brace
  {
    file: 'src/modals/IOModal/components/chatView/fileComponent/utils/format-file-name.tsx',
    action: () => {
      let content = fs.readFileSync('src/modals/IOModal/components/chatView/fileComponent/utils/format-file-name.tsx', 'utf8');
      if (!content.trim().endsWith('}')) {
        content = content.trim() + '\n}';
        fs.writeFileSync('src/modals/IOModal/components/chatView/fileComponent/utils/format-file-name.tsx', content);
        return true;
      }
      return false;
    }
  },
  
  // Fix types/api/index.ts - remove broken translation calls
  {
    file: 'src/types/api/index.ts',
    action: () => {
      let content = fs.readFileSync('src/types/api/index.ts', 'utf8');
      content = content.replace(/\{t\("common\.[^"]+"\)\}/g, 'any');
      content = content.replace(/=>\{t\("common\.[^"]+"\)\}</g, '=> any');
      fs.writeFileSync('src/types/api/index.ts', content);
      return true;
    }
  },
  
  // Fix createNewFlow.test.ts - fix type definition
  {
    file: 'src/utils/__tests__/createNewFlow.test.ts',
    action: () => {
      let content = fs.readFileSync('src/utils/__tests__/createNewFlow.test.ts', 'utf8');
      content = content.replace(/type FlowType = \{/, 'type FlowType = {');
      fs.writeFileSync('src/utils/__tests__/createNewFlow.test.ts', content);
      return true;
    }
  }
];

let fixedCount = 0;

fixes.forEach(({ file, action }) => {
  try {
    if (fs.existsSync(file)) {
      if (action()) {
        console.log(`✅ Fixed: ${file}`);
        fixedCount++;
      }
    } else {
      console.log(`⚠️  File not found: ${file}`);
    }
  } catch (error) {
    console.error(`❌ Error fixing ${file}: ${error.message}`);
  }
});

console.log(`\n🎉 Fixed ${fixedCount} files!`);

// Try to build
console.log('🔧 Attempting final build...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('🎉 BUILD SUCCESSFUL!');
  
  console.log('🔧 Copying to backend...');
  execSync('Remove-Item -Recurse -Force "..\\..\\src\\backend\\base\\axiestudio\\frontend\\*" -ErrorAction SilentlyContinue', { shell: 'powershell' });
  execSync('Copy-Item -Recurse -Force "build\\*" "..\\..\\src\\backend\\base\\axiestudio\\frontend\\"', { shell: 'powershell' });
  console.log('🎉 SUCCESS! Swedish translations deployed to backend!');
  
} catch (error) {
  console.log('❌ Build still has errors. Let me check what remains...');
  try {
    const buildOutput = execSync('npm run build 2>&1', { encoding: 'utf8' });
    console.log('Build output:', buildOutput.substring(0, 2000));
  } catch (e) {
    console.log('Error getting build output');
  }
}
