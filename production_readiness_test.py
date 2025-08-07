#!/usr/bin/env python3
"""
PRODUCTION READINESS TEST for Axie Studio
Comprehensive test to verify ALL components are properly imported and executable.
This test ensures NO "component failed to import" or "component not found" errors.
"""

import sys
import asyncio
import importlib
from pathlib import Path
from typing import Dict, List, Tuple

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

class ProductionReadinessTest:
    def __init__(self):
        self.total_components = 0
        self.successful_imports = 0
        self.failed_imports = []
        self.successful_instantiations = 0
        self.failed_instantiations = []
        
    def test_component_import_and_instantiation(self, name: str, module_path: str, class_name: str) -> bool:
        """Test if a component can be imported and instantiated."""
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the component class
            if not hasattr(module, class_name):
                self.failed_imports.append(f"{name}: Class '{class_name}' not found in module '{module_path}'")
                return False
            
            component_class = getattr(module, class_name)
            self.successful_imports += 1
            
            # Try to instantiate
            component_instance = component_class()
            
            # Verify it has required attributes
            required_attrs = ['display_name', 'description', 'name']
            for attr in required_attrs:
                if not hasattr(component_instance, attr):
                    self.failed_instantiations.append(f"{name}: Missing required attribute '{attr}'")
                    return False
            
            self.successful_instantiations += 1
            print(f"✅ {name}: Import and instantiation successful")
            return True
            
        except ImportError as e:
            self.failed_imports.append(f"{name}: Import failed - {e}")
            print(f"❌ {name}: Import failed - {e}")
            return False
        except Exception as e:
            self.failed_instantiations.append(f"{name}: Instantiation failed - {e}")
            print(f"❌ {name}: Instantiation failed - {e}")
            return False

    def test_all_components(self) -> bool:
        """Test ALL components for production readiness."""
        print("🚀 PRODUCTION READINESS TEST - ALL COMPONENTS")
        print("=" * 80)
        
        # Complete list of ALL components in Axie Studio
        all_components = [
            # INPUT/OUTPUT COMPONENTS
            ("Text Input", "axiestudio.components.input_output.text", "TextInputComponent"),
            ("Text Output", "axiestudio.components.input_output.text_output", "TextOutputComponent"),
            ("Chat Input", "axiestudio.components.input_output.chat", "ChatInput"),
            ("Chat Output", "axiestudio.components.input_output.chat_output", "ChatOutput"),
            
            # AI MODEL PROVIDERS
            ("OpenAI Chat", "axiestudio.components.openai.openai_chat_model", "OpenAIModelComponent"),
            ("OpenAI Embeddings", "axiestudio.components.openai.openai", "OpenAIEmbeddingsComponent"),
            ("Anthropic", "axiestudio.components.anthropic.anthropic", "AnthropicModelComponent"),
            ("Google Gemini", "axiestudio.components.google.google_generative_ai", "GoogleGenerativeAIComponent"),
            ("Google Embeddings", "axiestudio.components.google.google_generative_ai_embeddings", "GoogleGenerativeAIEmbeddingsComponent"),
            ("Groq", "axiestudio.components.groq.groq", "GroqModel"),
            ("Mistral", "axiestudio.components.mistral.mistral", "MistralAIModelComponent"),
            ("Mistral Embeddings", "axiestudio.components.mistral.mistral_embeddings", "MistralAIEmbeddingsComponent"),
            ("Cohere Chat", "axiestudio.components.cohere.cohere_models", "CohereComponent"),
            ("Cohere Embeddings", "axiestudio.components.cohere.cohere_embeddings", "CohereEmbeddingsComponent"),
            ("Azure OpenAI", "axiestudio.components.azure.azure_openai", "AzureChatOpenAIComponent"),
            ("Azure Embeddings", "axiestudio.components.azure.azure_openai_embeddings", "AzureOpenAIEmbeddingsComponent"),
            ("Ollama", "axiestudio.components.ollama.ollama", "ChatOllamaComponent"),
            ("Ollama Embeddings", "axiestudio.components.ollama.ollama_embeddings", "OllamaEmbeddingsComponent"),
            ("Hugging Face", "axiestudio.components.huggingface.huggingface", "HuggingFaceEndpointsComponent"),
            ("Amazon Bedrock", "axiestudio.components.amazon.amazon_bedrock_model", "AmazonBedrockComponent"),
            ("Amazon Bedrock Embeddings", "axiestudio.components.amazon.amazon_bedrock_embedding", "AmazonBedrockEmbeddingsComponent"),
            ("NVIDIA", "axiestudio.components.nvidia.nvidia", "NVIDIAModelComponent"),
            ("NVIDIA Embeddings", "axiestudio.components.nvidia.nvidia_embedding", "NVIDIAEmbeddingsComponent"),
            ("Vertex AI", "axiestudio.components.vertexai.vertexai", "ChatVertexAIComponent"),
            ("Vertex AI Embeddings", "axiestudio.components.vertexai.vertexai_embeddings", "VertexAIEmbeddingsComponent"),
            
            # VECTOR STORES
            ("Chroma", "axiestudio.components.vectorstores.chroma", "ChromaVectorStoreComponent"),
            ("Pinecone", "axiestudio.components.vectorstores.pinecone", "PineconeVectorStoreComponent"),
            ("FAISS", "axiestudio.components.vectorstores.faiss", "FaissVectorStoreComponent"),
            ("Qdrant", "axiestudio.components.vectorstores.qdrant", "QdrantVectorStoreComponent"),
            ("Weaviate", "axiestudio.components.vectorstores.weaviate", "WeaviateVectorStoreComponent"),
            ("AstraDB", "axiestudio.components.vectorstores.astradb", "AstraDBVectorStoreComponent"),
            ("MongoDB Atlas", "axiestudio.components.vectorstores.mongodb_atlas", "MongoVectorStoreComponent"),
            ("Elasticsearch", "axiestudio.components.vectorstores.elasticsearch", "ElasticsearchVectorStoreComponent"),
            ("Redis", "axiestudio.components.vectorstores.redis", "RedisVectorStoreComponent"),
            ("Supabase", "axiestudio.components.vectorstores.supabase", "SupabaseVectorStoreComponent"),
            
            # PROCESSING COMPONENTS
            ("Prompt", "axiestudio.components.processing.prompt", "PromptComponent"),
            ("Text Splitter", "axiestudio.components.processing.split_text", "SplitTextComponent"),
            ("Parse Data", "axiestudio.components.processing.parse_data", "ParseDataComponent"),
            ("Combine Text", "axiestudio.components.processing.combine_text", "CombineTextComponent"),
            ("Extract Key", "axiestudio.components.processing.extract_key", "ExtractDataKeyComponent"),
            ("Filter Data", "axiestudio.components.processing.filter_data", "FilterDataComponent"),
            ("Create Data", "axiestudio.components.processing.create_data", "CreateDataComponent"),
            ("Update Data", "axiestudio.components.processing.update_data", "UpdateDataComponent"),
            ("Merge Data", "axiestudio.components.processing.merge_data", "MergeDataComponent"),
            
            # DATA SOURCES
            ("File", "axiestudio.components.data.file", "FileComponent"),
            ("URL", "axiestudio.components.data.url", "URLComponent"),
            ("API Request", "axiestudio.components.data.api_request", "APIRequestComponent"),
            ("CSV to Data", "axiestudio.components.data.csv_to_data", "CSVToDataComponent"),
            ("JSON to Data", "axiestudio.components.data.json_to_data", "JSONToDataComponent"),
            ("Directory", "axiestudio.components.data.directory", "DirectoryComponent"),
            ("Web Search", "axiestudio.components.data.web_search", "WebSearchComponent"),
            
            # LOGIC COMPONENTS
            ("Conditional Router", "axiestudio.components.logic.conditional_router", "ConditionalRouterComponent"),
            ("Pass Message", "axiestudio.components.logic.pass_message", "PassMessageComponent"),
            ("Sub Flow", "axiestudio.components.logic.sub_flow", "SubFlowComponent"),
            ("Run Flow", "axiestudio.components.logic.run_flow", "RunFlowComponent"),
            ("Listen", "axiestudio.components.logic.listen", "ListenComponent"),
            ("Notify", "axiestudio.components.logic.notify", "NotifyComponent"),
            
            # HELPER COMPONENTS
            ("Memory", "axiestudio.components.helpers.memory", "MemoryComponent"),
            ("Current Date", "axiestudio.components.helpers.current_date", "CurrentDateComponent"),
            ("ID Generator", "axiestudio.components.helpers.id_generator", "IDGeneratorComponent"),
            ("Calculator", "axiestudio.components.helpers.calculator_core", "CalculatorComponent"),
            ("Create List", "axiestudio.components.helpers.create_list", "CreateListComponent"),
            
            # AGENTS
            ("Agent", "axiestudio.components.agents.agent", "AgentComponent"),
            
            # EMBEDDINGS
            ("Text Embedder", "axiestudio.components.embeddings.text_embedder", "TextEmbedderComponent"),
            ("Similarity", "axiestudio.components.embeddings.similarity", "EmbeddingSimilarityComponent"),
        ]
        
        self.total_components = len(all_components)
        print(f"📊 Testing {self.total_components} components for production readiness...")
        print()
        
        # Test each component
        success_count = 0
        for name, module_path, class_name in all_components:
            if self.test_component_import_and_instantiation(name, module_path, class_name):
                success_count += 1
        
        return success_count == self.total_components

    def print_results(self):
        """Print comprehensive test results."""
        print("\n" + "=" * 80)
        print("📊 PRODUCTION READINESS TEST RESULTS")
        print("=" * 80)
        
        print(f"📦 Total Components Tested: {self.total_components}")
        print(f"✅ Successful Imports: {self.successful_imports}/{self.total_components}")
        print(f"✅ Successful Instantiations: {self.successful_instantiations}/{self.total_components}")
        
        if self.failed_imports:
            print(f"\n❌ FAILED IMPORTS ({len(self.failed_imports)}):")
            for failure in self.failed_imports:
                print(f"   • {failure}")
        
        if self.failed_instantiations:
            print(f"\n❌ FAILED INSTANTIATIONS ({len(self.failed_instantiations)}):")
            for failure in self.failed_instantiations:
                print(f"   • {failure}")
        
        success_rate = (self.successful_instantiations / self.total_components) * 100
        print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 PRODUCTION READY: ALL COMPONENTS WORKING!")
            print("✅ NO 'component failed to import' errors")
            print("✅ NO 'component not found' errors")
            print("✅ ALL components properly downloaded and executable")
        elif success_rate >= 95:
            print("⚠️  MOSTLY PRODUCTION READY: Minor issues detected")
        else:
            print("❌ NOT PRODUCTION READY: Significant issues detected")

def main():
    """Run the production readiness test."""
    test = ProductionReadinessTest()
    
    try:
        all_working = test.test_all_components()
        test.print_results()
        
        return all_working
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
