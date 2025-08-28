#!/usr/bin/env node
/**
 * Langflow to AxieStudio Component Converter
 * Converts downloaded Langflow Store components to work with AxieStudio backend
 */

const fs = require('fs').promises;
const path = require('path');

// Comprehensive mapping of Langflow imports to AxieStudio equivalents
const IMPORT_MAPPINGS = {
    // Main module mappings
    'langflow': 'axiestudio',
    
    // Specific import patterns
    'from langflow.custom import': 'from axiestudio.custom import',
    'from langflow.base.models.model import': 'from axiestudio.base.models.model import',
    'from langflow.inputs.inputs import': 'from axiestudio.inputs.inputs import',
    'from langflow.io import': 'from axiestudio.io import',
    'from langflow.schema.data import': 'from axiestudio.schema.data import',
    'from langflow.schema.message import': 'from axiestudio.schema.message import',
    'from langflow.schema.dataframe import': 'from axiestudio.schema.dataframe import',
    'from langflow.field_typing import': 'from axiestudio.field_typing import',
    'from langflow.template import': 'from axiestudio.template import',
    'from langflow.components import': 'from axiestudio.components import',
    'from langflow.custom.custom_component.component import': 'from axiestudio.custom.custom_component.component import',
    'from langflow.base.langchain_utilities.model import': 'from axiestudio.base.langchain_utilities.model import',
    'from langflow.helpers import': 'from axiestudio.helpers import',
    'from langflow.logging import': 'from axiestudio.logging import',
    'from langflow.utils import': 'from axiestudio.utils import',
    'from langflow.field_typing.range_spec import': 'from axiestudio.field_typing.range_spec import',
    
    // Nested imports
    'langflow.custom': 'axiestudio.custom',
    'langflow.base': 'axiestudio.base',
    'langflow.inputs': 'axiestudio.inputs',
    'langflow.io': 'axiestudio.io',
    'langflow.schema': 'axiestudio.schema',
    'langflow.field_typing': 'axiestudio.field_typing',
    'langflow.template': 'axiestudio.template',
    'langflow.components': 'axiestudio.components',
    'langflow.helpers': 'axiestudio.helpers',
    'langflow.logging': 'axiestudio.logging',
    'langflow.utils': 'axiestudio.utils',
};

// Additional patterns for more complex replacements
const PATTERN_MAPPINGS = [
    // Import statements
    {
        pattern: /from\s+langflow\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import/g,
        replacement: 'from axiestudio.$1 import'
    },
    {
        pattern: /import\s+langflow\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)/g,
        replacement: 'import axiestudio.$1'
    },
    // String references
    {
        pattern: /"langflow\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)"/g,
        replacement: '"axiestudio.$1"'
    },
    {
        pattern: /'langflow\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'/g,
        replacement: "'axiestudio.$1'"
    },
    // Documentation URLs
    {
        pattern: /https:\/\/docs\.langflow\.org/g,
        replacement: 'https://docs.axiestudio.org'
    },
    {
        pattern: /https:\/\/langflow\.org/g,
        replacement: 'https://axiestudio.org'
    }
];

class LangflowToAxieStudioConverter {
    constructor() {
        this.sourceDir = path.join('src', 'store_components');
        this.outputDir = path.join('src', 'store_components_converted');
        this.conversionStats = {
            totalFiles: 0,
            convertedFiles: 0,
            skippedFiles: 0,
            errors: 0,
            conversions: 0
        };
    }

    async ensureOutputDir() {
        try {
            await fs.mkdir(this.outputDir, { recursive: true });
            await fs.mkdir(path.join(this.outputDir, 'flows'), { recursive: true });
            await fs.mkdir(path.join(this.outputDir, 'components'), { recursive: true });
            
            console.log(`📁 Created conversion output directories:`);
            console.log(`   - ${this.outputDir}`);
            console.log(`   - ${path.join(this.outputDir, 'flows')}`);
            console.log(`   - ${path.join(this.outputDir, 'components')}`);
        } catch (error) {
            console.error(`❌ Failed to create output directory: ${error.message}`);
            throw error;
        }
    }

    convertCode(code) {
        if (!code || typeof code !== 'string') {
            return code;
        }

        let convertedCode = code;
        let conversionsCount = 0;

        // Apply direct string mappings first
        for (const [langflowImport, axiestudioImport] of Object.entries(IMPORT_MAPPINGS)) {
            const regex = new RegExp(langflowImport.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
            const matches = convertedCode.match(regex);
            if (matches) {
                convertedCode = convertedCode.replace(regex, axiestudioImport);
                conversionsCount += matches.length;
            }
        }

        // Apply pattern mappings
        for (const mapping of PATTERN_MAPPINGS) {
            const matches = convertedCode.match(mapping.pattern);
            if (matches) {
                convertedCode = convertedCode.replace(mapping.pattern, mapping.replacement);
                conversionsCount += matches.length;
            }
        }

        return { convertedCode, conversionsCount };
    }

    async convertComponent(componentData) {
        try {
            let totalConversions = 0;
            const convertedComponent = JSON.parse(JSON.stringify(componentData)); // Deep clone

            // Convert the main component data code
            if (convertedComponent.data && typeof convertedComponent.data === 'object') {
                const dataStr = JSON.stringify(convertedComponent.data);
                const { convertedCode: convertedDataStr, conversionsCount } = this.convertCode(dataStr);
                
                if (conversionsCount > 0) {
                    convertedComponent.data = JSON.parse(convertedDataStr);
                    totalConversions += conversionsCount;
                }
            }

            // Convert any code fields in the original component
            if (convertedComponent.original && convertedComponent.original.data) {
                const originalDataStr = JSON.stringify(convertedComponent.original.data);
                const { convertedCode: convertedOriginalStr, conversionsCount: originalConversions } = this.convertCode(originalDataStr);
                
                if (originalConversions > 0) {
                    convertedComponent.original.data = JSON.parse(convertedOriginalStr);
                    totalConversions += originalConversions;
                }
            }

            // Add conversion metadata
            convertedComponent.conversion = {
                converted_at: new Date().toISOString(),
                converted_from: 'langflow',
                converted_to: 'axiestudio',
                conversions_made: totalConversions,
                converter_version: '1.0.0'
            };

            // Update description to indicate conversion
            if (convertedComponent.description) {
                convertedComponent.description += ' (Converted from Langflow Store for AxieStudio compatibility)';
            }

            return { convertedComponent, conversionsCount: totalConversions };

        } catch (error) {
            console.error(`❌ Error converting component: ${error.message}`);
            throw error;
        }
    }

    async processFile(filePath, outputPath) {
        try {
            this.conversionStats.totalFiles++;
            
            console.log(`🔄 Processing: ${path.basename(filePath)}`);
            
            const fileContent = await fs.readFile(filePath, 'utf8');
            const componentData = JSON.parse(fileContent);
            
            const { convertedComponent, conversionsCount } = await this.convertComponent(componentData);
            
            if (conversionsCount > 0) {
                await fs.writeFile(outputPath, JSON.stringify(convertedComponent, null, 2), 'utf8');
                console.log(`✅ Converted: ${path.basename(filePath)} (${conversionsCount} conversions)`);
                this.conversionStats.convertedFiles++;
                this.conversionStats.conversions += conversionsCount;
            } else {
                // Still copy the file but mark as no conversions needed
                await fs.writeFile(outputPath, JSON.stringify(convertedComponent, null, 2), 'utf8');
                console.log(`📋 Copied: ${path.basename(filePath)} (no conversions needed)`);
                this.conversionStats.skippedFiles++;
            }

        } catch (error) {
            console.error(`❌ Error processing ${filePath}: ${error.message}`);
            this.conversionStats.errors++;
        }
    }

    async convertAllComponents() {
        try {
            console.log("🚀 Starting Langflow to AxieStudio conversion...");
            
            // Process flows
            const flowsDir = path.join(this.sourceDir, 'flows');
            const outputFlowsDir = path.join(this.outputDir, 'flows');
            
            try {
                const flowFiles = await fs.readdir(flowsDir);
                const jsonFlowFiles = flowFiles.filter(file => file.endsWith('.json') && file !== 'flows_index.json');
                
                console.log(`📊 Converting ${jsonFlowFiles.length} flows...`);
                
                for (const file of jsonFlowFiles) {
                    const inputPath = path.join(flowsDir, file);
                    const outputPath = path.join(outputFlowsDir, file);
                    await this.processFile(inputPath, outputPath);
                }
            } catch (error) {
                console.log(`⚠️  No flows directory found or error reading flows: ${error.message}`);
            }

            // Process components
            const componentsDir = path.join(this.sourceDir, 'components');
            const outputComponentsDir = path.join(this.outputDir, 'components');
            
            try {
                const componentFiles = await fs.readdir(componentsDir);
                const jsonComponentFiles = componentFiles.filter(file => file.endsWith('.json') && file !== 'components_index.json');
                
                console.log(`📊 Converting ${jsonComponentFiles.length} components...`);
                
                for (const file of jsonComponentFiles) {
                    const inputPath = path.join(componentsDir, file);
                    const outputPath = path.join(outputComponentsDir, file);
                    await this.processFile(inputPath, outputPath);
                }
            } catch (error) {
                console.log(`⚠️  No components directory found or error reading components: ${error.message}`);
            }

            // Copy and convert index files
            await this.convertIndexFiles();

        } catch (error) {
            console.error(`❌ Conversion failed: ${error.message}`);
            throw error;
        }
    }

    async convertIndexFiles() {
        try {
            // Convert main store index
            const mainIndexPath = path.join(this.sourceDir, 'store_index.json');
            const outputMainIndexPath = path.join(this.outputDir, 'store_index.json');
            
            if (await this.fileExists(mainIndexPath)) {
                const indexContent = await fs.readFile(mainIndexPath, 'utf8');
                const indexData = JSON.parse(indexContent);
                
                // Add conversion info to index
                indexData.conversion_info = {
                    converted_at: new Date().toISOString(),
                    converted_from: 'langflow',
                    converted_to: 'axiestudio',
                    original_source: 'Langflow Store',
                    converter_version: '1.0.0'
                };
                
                await fs.writeFile(outputMainIndexPath, JSON.stringify(indexData, null, 2), 'utf8');
                console.log(`📋 Converted main index file`);
            }

            // Convert flows index
            const flowsIndexPath = path.join(this.sourceDir, 'flows', 'flows_index.json');
            const outputFlowsIndexPath = path.join(this.outputDir, 'flows', 'flows_index.json');
            
            if (await this.fileExists(flowsIndexPath)) {
                const indexContent = await fs.readFile(flowsIndexPath, 'utf8');
                const indexData = JSON.parse(indexContent);
                
                indexData.conversion_info = {
                    converted_at: new Date().toISOString(),
                    converted_from: 'langflow',
                    converted_to: 'axiestudio'
                };
                
                await fs.writeFile(outputFlowsIndexPath, JSON.stringify(indexData, null, 2), 'utf8');
                console.log(`📋 Converted flows index file`);
            }

            // Convert components index
            const componentsIndexPath = path.join(this.sourceDir, 'components', 'components_index.json');
            const outputComponentsIndexPath = path.join(this.outputDir, 'components', 'components_index.json');
            
            if (await this.fileExists(componentsIndexPath)) {
                const indexContent = await fs.readFile(componentsIndexPath, 'utf8');
                const indexData = JSON.parse(indexContent);
                
                indexData.conversion_info = {
                    converted_at: new Date().toISOString(),
                    converted_from: 'langflow',
                    converted_to: 'axiestudio'
                };
                
                await fs.writeFile(outputComponentsIndexPath, JSON.stringify(indexData, null, 2), 'utf8');
                console.log(`📋 Converted components index file`);
            }

        } catch (error) {
            console.error(`❌ Error converting index files: ${error.message}`);
        }
    }

    async fileExists(filePath) {
        try {
            await fs.access(filePath);
            return true;
        } catch {
            return false;
        }
    }

    printStats() {
        console.log("\n" + "=".repeat(60));
        console.log("🎉 CONVERSION COMPLETED!");
        console.log("=".repeat(60));
        console.log(`📊 STATISTICS:`);
        console.log(`   📁 Total files processed: ${this.conversionStats.totalFiles}`);
        console.log(`   ✅ Files converted: ${this.conversionStats.convertedFiles}`);
        console.log(`   📋 Files copied (no conversion needed): ${this.conversionStats.skippedFiles}`);
        console.log(`   ❌ Errors: ${this.conversionStats.errors}`);
        console.log(`   🔄 Total conversions made: ${this.conversionStats.conversions}`);
        console.log(`\n📁 Converted files saved to: ${path.resolve(this.outputDir)}`);
        console.log("=".repeat(60));
    }

    async run() {
        try {
            await this.ensureOutputDir();
            await this.convertAllComponents();
            this.printStats();
            
            if (this.conversionStats.errors > 0) {
                console.log(`\n⚠️  ${this.conversionStats.errors} errors occurred during conversion. Check the logs above.`);
            }
            
            console.log("\n🎯 Next steps:");
            console.log("1. Review converted components in the output directory");
            console.log("2. Test a few converted components in AxieStudio");
            console.log("3. Create a browsing interface for the converted components");
            
        } catch (error) {
            console.error(`❌ Conversion failed: ${error.message}`);
            throw error;
        }
    }
}

// Main execution
async function main() {
    const converter = new LangflowToAxieStudioConverter();
    await converter.run();
}

// Run if this file is executed directly
if (require.main === module) {
    main().catch(error => {
        console.error('❌ Fatal error:', error.message);
        process.exit(1);
    });
}

module.exports = LangflowToAxieStudioConverter;
