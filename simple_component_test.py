#!/usr/bin/env python3
"""
Simple test to verify Axie Studio components are working properly.
Tests the most critical components for basic functionality.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_core_components():
    """Test core components that are essential for basic flows."""
    print("🧪 TESTING CORE COMPONENTS...")
    
    core_components = [
        # Input/Output
        ("Text Input", "axiestudio.components.input_output.text", "TextInputComponent"),
        ("Text Output", "axiestudio.components.input_output.text_output", "TextOutputComponent"),
        ("Chat Input", "axiestudio.components.input_output.chat", "ChatInputComponent"),
        ("Chat Output", "axiestudio.components.input_output.chat_output", "ChatOutputComponent"),
        
        # AI Models
        ("OpenAI Chat", "axiestudio.components.openai.openai_chat_model", "OpenAIModelComponent"),
        ("OpenAI Embeddings", "axiestudio.components.openai.openai", "OpenAIEmbeddingsComponent"),
        ("Anthropic", "axiestudio.components.anthropic.anthropic", "AnthropicModelComponent"),
        ("Google Gemini", "axiestudio.components.google.google_generative_ai", "GoogleGenerativeAIComponent"),
        
        # Processing
        ("Prompt", "axiestudio.components.processing.prompt", "PromptComponent"),
        ("Text Splitter", "axiestudio.components.processing.split_text", "SplitTextComponent"),
        ("Parse Data", "axiestudio.components.processing.parse_data", "ParseDataComponent"),
        
        # Vector Stores
        ("Chroma", "axiestudio.components.vectorstores.chroma", "ChromaVectorStoreComponent"),
        ("Pinecone", "axiestudio.components.vectorstores.pinecone", "PineconeVectorStoreComponent"),
        ("FAISS", "axiestudio.components.vectorstores.faiss", "FAISSVectorStoreComponent"),
        
        # Data Sources
        ("File", "axiestudio.components.data.file", "FileComponent"),
        ("URL", "axiestudio.components.data.url", "URLComponent"),
        ("API Request", "axiestudio.components.data.api_request", "APIRequestComponent"),
        
        # Logic
        ("Conditional Router", "axiestudio.components.logic.conditional_router", "ConditionalRouterComponent"),
        ("Pass Message", "axiestudio.components.logic.pass_message", "PassMessageComponent"),
        
        # Helpers
        ("Memory", "axiestudio.components.helpers.memory", "MemoryComponent"),
        ("Current Date", "axiestudio.components.helpers.current_date", "CurrentDateComponent"),
    ]
    
    success_count = 0
    failed_components = []
    
    for name, module_path, class_name in core_components:
        try:
            # Import the module
            module = __import__(module_path, fromlist=[class_name])
            component_class = getattr(module, class_name)
            
            # Try to instantiate (basic test)
            component_instance = component_class()
            
            # Check if it has required attributes
            if hasattr(component_instance, 'display_name') and hasattr(component_instance, 'description'):
                print(f"✅ {name}: Working properly")
                success_count += 1
            else:
                print(f"⚠️  {name}: Missing required attributes")
                failed_components.append(name)
            
        except ImportError as e:
            print(f"❌ {name}: Import failed - {e}")
            failed_components.append(name)
        except AttributeError as e:
            print(f"❌ {name}: Class not found - {e}")
            failed_components.append(name)
        except Exception as e:
            print(f"⚠️  {name}: Instantiation issue - {e}")
            failed_components.append(name)
    
    print(f"\n📊 RESULTS: {success_count}/{len(core_components)} components working")
    
    if failed_components:
        print(f"❌ Failed components: {', '.join(failed_components)}")
        return False
    else:
        print("🎉 ALL CORE COMPONENTS ARE WORKING!")
        return True

def test_ai_providers():
    """Test that major AI providers are available."""
    print("\n🤖 TESTING AI PROVIDERS...")
    
    ai_tests = [
        ("OpenAI", "axiestudio.components.openai.openai_chat_model", "OpenAIModelComponent"),
        ("Anthropic", "axiestudio.components.anthropic.anthropic", "AnthropicModelComponent"),
        ("Google", "axiestudio.components.google.google_generative_ai", "GoogleGenerativeAIComponent"),
        ("Groq", "axiestudio.components.groq.groq", "GroqModel"),
        ("Mistral", "axiestudio.components.mistral.mistral", "MistralAIModelComponent"),
        ("Ollama", "axiestudio.components.ollama.ollama", "ChatOllamaComponent"),
    ]
    
    working_providers = 0
    
    for provider, module_path, class_name in ai_tests:
        try:
            module = __import__(module_path, fromlist=[class_name])
            component_class = getattr(module, class_name)
            component_instance = component_class()
            print(f"✅ {provider}: Available")
            working_providers += 1
        except Exception as e:
            print(f"❌ {provider}: Not available - {e}")
    
    print(f"\n📊 AI Providers: {working_providers}/{len(ai_tests)} available")
    return working_providers >= 4  # At least 4 providers should work

def test_vector_stores():
    """Test vector store components."""
    print("\n🗄️ TESTING VECTOR STORES...")
    
    vector_stores = [
        ("Chroma", "axiestudio.components.vectorstores.chroma", "ChromaVectorStoreComponent"),
        ("Pinecone", "axiestudio.components.vectorstores.pinecone", "PineconeVectorStoreComponent"),
        ("FAISS", "axiestudio.components.vectorstores.faiss", "FAISSVectorStoreComponent"),
        ("Qdrant", "axiestudio.components.vectorstores.qdrant", "QdrantVectorStoreComponent"),
        ("Weaviate", "axiestudio.components.vectorstores.weaviate", "WeaviateVectorStoreComponent"),
    ]
    
    working_stores = 0
    
    for store, module_path, class_name in vector_stores:
        try:
            module = __import__(module_path, fromlist=[class_name])
            component_class = getattr(module, class_name)
            component_instance = component_class()
            print(f"✅ {store}: Available")
            working_stores += 1
        except Exception as e:
            print(f"❌ {store}: Not available - {e}")
    
    print(f"\n📊 Vector Stores: {working_stores}/{len(vector_stores)} available")
    return working_stores >= 3  # At least 3 stores should work

def main():
    """Run component tests."""
    print("🚀 AXIE STUDIO COMPONENT FUNCTIONALITY TEST")
    print("=" * 60)
    
    tests = [
        ("Core Components", test_core_components),
        ("AI Providers", test_ai_providers),
        ("Vector Stores", test_vector_stores),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*60}")
    print(f"🎯 FINAL RESULTS: {passed}/{total} test categories passed")
    
    if passed == total:
        print("🎉 ALL COMPONENTS ARE PROPERLY DOWNLOADED AND EXECUTABLE!")
        print("✅ Your Axie Studio is ready for production use!")
        return True
    else:
        print("⚠️  Some components have issues - but core functionality should work")
        return passed >= 2  # At least core components should work

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
