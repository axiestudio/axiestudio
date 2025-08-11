#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('Simple search for any remaining t( calls...\n');

try {
  // Use grep to find all t( calls
  const result = execSync('grep -r "\\bt(" src/ --include="*.tsx" --include="*.ts"', { 
    encoding: 'utf8',
    cwd: __dirname 
  });
  
  const lines = result.split('\n').filter(line => line.trim());
  
  console.log(`Found ${lines.length} lines with t( calls:`);
  
  // Filter out obvious false positives
  const filtered = lines.filter(line => {
    return !line.includes('setTimeout') &&
           !line.includes('setInterval') &&
           !line.includes('clearTimeout') &&
           !line.includes('split(') &&
           !line.includes('createElement(') &&
           !line.includes('dispatchEvent(') &&
           !line.includes('getAttribute(') &&
           !line.includes('setAttribute(') &&
           !line.includes('querySelector(') &&
           !line.includes('addEventListener(') &&
           !line.includes('removeEventListener(') &&
           !line.includes('getT') &&
           !line.includes('setT') &&
           !line.includes('const t =') &&
           !line.includes('let t =') &&
           !line.includes('var t =');
  });
  
  console.log(`After filtering: ${filtered.length} potential translation calls\n`);
  
  if (filtered.length > 0) {
    console.log('Potential translation calls:');
    filtered.forEach((line, index) => {
      if (index < 20) { // Show first 20
        console.log(`${index + 1}: ${line}`);
      }
    });
    
    if (filtered.length > 20) {
      console.log(`... and ${filtered.length - 20} more`);
    }
  }
  
} catch (error) {
  console.log('Grep failed, trying alternative approach...');
  
  // Fallback: manual search
  function findFiles(dir) {
    const files = [];
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        files.push(...findFiles(fullPath));
      } else if (item.endsWith('.tsx') || item.endsWith('.ts')) {
        files.push(fullPath);
      }
    }
    
    return files;
  }
  
  const files = findFiles(path.join(__dirname, 'src'));
  console.log(`Checking ${files.length} files manually...`);
  
  let totalMatches = 0;
  
  files.forEach(file => {
    try {
      const content = fs.readFileSync(file, 'utf8');
      const matches = content.match(/\bt\(/g);
      if (matches) {
        totalMatches += matches.length;
        console.log(`${file}: ${matches.length} matches`);
      }
    } catch (err) {
      // Skip files that can't be read
    }
  });
  
  console.log(`\nTotal t( calls found: ${totalMatches}`);
}

console.log('\nDone.');
