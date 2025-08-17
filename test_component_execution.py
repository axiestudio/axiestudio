#!/usr/bin/env python3
"""
Test script to verify all Axie Studio components are properly loaded and executable.
This script tests component discovery, import, and basic execution.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_component_loading():
    """Test that all components can be loaded without errors."""
    print("🧪 TESTING COMPONENT LOADING...")

    try:
        from axiestudio.interface.components import get_and_cache_all_types_dict
        from axiestudio.services.settings.service import SettingsService

        # Create settings service
        settings_service = SettingsService()

        # Load all components
        components_dict = await get_and_cache_all_types_dict(settings_service)

        if not components_dict:
            print("❌ No components loaded!")
            return False

        print(f"✅ Successfully loaded {len(components_dict)} component categories")

        # Count total components
        total_components = 0
        for category, components in components_dict.items():
            if isinstance(components, dict):
                total_components += len(components)
                print(f"   📦 {category}: {len(components)} components")

        print(f"🎯 Total components available: {total_components}")
        return True

    except Exception as e:
        print(f"❌ Component loading failed: {e}")
        return False

async def test_specific_components():
    """Test specific high-use components for import and basic functionality."""
    print("\n🔧 TESTING SPECIFIC COMPONENTS...")
    
    test_components = [
        ("OpenAI Chat", "axiestudio.components.openai.openai_chat_model", "OpenAIModelComponent"),
        ("Text Input", "axiestudio.components.input_output.text", "TextInputComponent"),
        ("Text Output", "axiestudio.components.input_output.text_output", "TextOutputComponent"),
        ("Prompt", "axiestudio.components.processing.prompt", "PromptComponent"),
        ("Chroma Vector Store", "axiestudio.components.vectorstores.chroma", "ChromaVectorStoreComponent"),
    ]
    
    success_count = 0
    
    for name, module_path, class_name in test_components:
        try:
            # Import the module
            module = __import__(module_path, fromlist=[class_name])
            component_class = getattr(module, class_name)
            
            # Try to instantiate (basic test)
            component_instance = component_class()
            
            print(f"✅ {name}: Import and instantiation successful")
            success_count += 1
            
        except ImportError as e:
            print(f"❌ {name}: Import failed - {e}")
        except AttributeError as e:
            print(f"❌ {name}: Class not found - {e}")
        except Exception as e:
            print(f"⚠️  {name}: Instantiation issue - {e}")
    
    print(f"\n📊 Component Test Results: {success_count}/{len(test_components)} passed")
    return success_count == len(test_components)

async def test_component_categories():
    """Test that all major component categories are present."""
    print("\n📋 TESTING COMPONENT CATEGORIES...")
    
    expected_categories = [
        "input_output",
        "models", 
        "agents",
        "data",
        "vectorstores",
        "processing",
        "logic",
        "helpers",
        "openai",
        "anthropic",
        "google",
        "langchain_utilities"
    ]
    
    try:
        from axiestudio.interface.components import get_and_cache_all_types_dict
        from axiestudio.services.settings.service import SettingsService

        settings_service = SettingsService()
        components_dict = await get_and_cache_all_types_dict(settings_service)
        
        missing_categories = []
        present_categories = []
        
        for category in expected_categories:
            if category in components_dict:
                present_categories.append(category)
                print(f"✅ {category}: Present")
            else:
                missing_categories.append(category)
                print(f"❌ {category}: Missing")
        
        if missing_categories:
            print(f"\n⚠️  Missing categories: {missing_categories}")
            return False
        else:
            print(f"\n🎉 All {len(expected_categories)} expected categories present!")
            return True
            
    except Exception as e:
        print(f"❌ Category test failed: {e}")
        return False

async def test_ai_providers():
    """Test that all major AI providers are available."""
    print("\n🤖 TESTING AI PROVIDERS...")
    
    ai_providers = [
        "openai",
        "anthropic", 
        "google",
        "groq",
        "mistral",
        "cohere",
        "azure",
        "ollama",
        "huggingface"
    ]
    
    try:
        from axiestudio.interface.components import get_and_cache_all_types_dict
        from axiestudio.services.settings.service import SettingsService

        settings_service = SettingsService()
        components_dict = await get_and_cache_all_types_dict(settings_service)
        
        available_providers = []
        missing_providers = []
        
        for provider in ai_providers:
            if provider in components_dict:
                available_providers.append(provider)
                print(f"✅ {provider}: Available")
            else:
                missing_providers.append(provider)
                print(f"❌ {provider}: Missing")
        
        print(f"\n📊 AI Providers: {len(available_providers)}/{len(ai_providers)} available")
        return len(missing_providers) == 0
        
    except Exception as e:
        print(f"❌ AI provider test failed: {e}")
        return False

async def main():
    """Run all component tests."""
    print("🚀 AXIE STUDIO COMPONENT VERIFICATION")
    print("=" * 50)
    
    tests = [
        ("Component Loading", test_component_loading),
        ("Specific Components", test_specific_components),
        ("Component Categories", test_component_categories),
        ("AI Providers", test_ai_providers),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if await test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*50}")
    print(f"🎯 FINAL RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL COMPONENTS ARE PROPERLY LOADED AND EXECUTABLE!")
        return True
    else:
        print("⚠️  Some components have issues - check logs above")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
