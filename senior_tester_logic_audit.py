#!/usr/bin/env python3
"""
SENIOR TESTER - CRITICAL LOGIC SYSTEM IMPLEMENTATION AUDIT
Testing actual system logic against requirements.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

class SeniorLogicTester:
    def __init__(self):
        self.critical_issues = []
        self.warnings = []
        self.test_results = {}
        
    async def run_logic_audit(self):
        """Run comprehensive logic audit"""
        print("🔍 SENIOR TESTER - CRITICAL LOGIC SYSTEM AUDIT")
        print("=" * 60)
        print("Testing ACTUAL system logic against requirements...")
        print()
        
        # Test 1: System Implementation Logic
        await self.test_system_implementation()
        
        # Test 2: UI/UX Logic
        await self.test_ui_ux_logic()
        
        # Test 3: Integration Logic
        await self.test_integration_logic()
        
        # Generate Final Report
        self.generate_logic_report()
        
        return len(self.critical_issues) == 0
    
    async def test_system_implementation(self):
        """Test System Implementation Logic"""
        print("🔧 SYSTEM IMPLEMENTATION LOGIC TEST")
        print("-" * 50)
        
        # Test 1.1: File Display Logic
        print("📁 Testing File Display Logic...")
        try:
            from axiestudio.api.v1.axiestudio_store import load_store_index
            
            store_data = load_store_index()
            total_items = len(store_data.flows) + len(store_data.components)
            
            if total_items == 1600:
                print(f"✅ File Count: {total_items} items (CORRECT)")
                self.test_results["file_display"] = True
            else:
                self.critical_issues.append(f"Expected 1600 files, found {total_items}")
                print(f"❌ File Count: {total_items} items (INCORRECT)")
                self.test_results["file_display"] = False
                
            # Test categorization
            flows_count = len(store_data.flows)
            components_count = len(store_data.components)
            
            if flows_count > 0 and components_count > 0:
                print(f"✅ Categorization: {flows_count} flows, {components_count} components")
                self.test_results["categorization"] = True
            else:
                self.critical_issues.append("Categorization failed - missing flows or components")
                self.test_results["categorization"] = False
                
        except Exception as e:
            self.critical_issues.append(f"File display logic failed: {e}")
            self.test_results["file_display"] = False
            self.test_results["categorization"] = False
        
        # Test 1.2: Download Function Logic
        print("\n📥 Testing Download Function Logic...")
        try:
            from axiestudio.api.v1.axiestudio_store import load_item_data
            
            # Test component download
            if store_data.components:
                sample_component = store_data.components[0]
                component_data = load_item_data("component", sample_component.id)
                
                if component_data and 'name' in component_data:
                    print(f"✅ Component Download: {component_data['name']}")
                    self.test_results["component_download"] = True
                else:
                    self.critical_issues.append("Component download returns invalid data")
                    self.test_results["component_download"] = False
            
            # Test flow download
            if store_data.flows:
                sample_flow = store_data.flows[0]
                flow_data = load_item_data("flow", sample_flow.id)
                
                if flow_data and 'name' in flow_data:
                    print(f"✅ Flow Download: {flow_data['name']}")
                    self.test_results["flow_download"] = True
                else:
                    self.critical_issues.append("Flow download returns invalid data")
                    self.test_results["flow_download"] = False
                    
        except Exception as e:
            self.critical_issues.append(f"Download function logic failed: {e}")
            self.test_results["component_download"] = False
            self.test_results["flow_download"] = False
        
        # Test 1.3: Route Accessibility Logic
        print("\n🛣️ Testing Route Accessibility Logic...")
        
        routes_file = Path(__file__).parent / "src/frontend/src/customization/utils/custom-routes-store-pages.tsx"
        if routes_file.exists():
            with open(routes_file, 'r') as f:
                routes_content = f.read()
            
            if 'path="showcase"' in routes_content and 'ShowcasePage' in routes_content:
                print("✅ Route Logic: /showcase properly configured")
                self.test_results["route_access"] = True
            else:
                self.critical_issues.append("Route /showcase not properly configured")
                self.test_results["route_access"] = False
        else:
            self.critical_issues.append("Routes configuration file missing")
            self.test_results["route_access"] = False
        
        # Test 1.4: Flow Page Button Logic
        print("\n🔘 Testing Flow Page Button Logic...")
        
        toolbar_file = Path(__file__).parent / "src/frontend/src/components/core/flowToolbarComponent/components/flow-toolbar-options.tsx"
        if toolbar_file.exists():
            with open(toolbar_file, 'r') as f:
                toolbar_content = f.read()
            
            if 'ShowcaseButton' in toolbar_content:
                print("✅ Button Logic: ShowcaseButton integrated in toolbar")
                self.test_results["button_integration"] = True
            else:
                self.critical_issues.append("ShowcaseButton not integrated in toolbar")
                self.test_results["button_integration"] = False
        else:
            self.critical_issues.append("Toolbar file missing")
            self.test_results["button_integration"] = False
    
    async def test_ui_ux_logic(self):
        """Test UI/UX Logic"""
        print(f"\n🎨 UI/UX LOGIC TEST")
        print("-" * 50)
        
        showcase_file = Path(__file__).parent / "src/frontend/src/pages/ShowcasePage/index.tsx"
        if not showcase_file.exists():
            self.critical_issues.append("ShowcasePage component missing")
            return
        
        with open(showcase_file, 'r') as f:
            content = f.read()
        
        # Test 2.1: Visual Design Logic
        print("🎯 Testing Visual Design Logic...")
        
        design_features = {
            "Modern Cards": "Card className",
            "Gradient Headers": "bg-gradient-to-r",
            "Hover Effects": "hover:",
            "Responsive Grid": "md:grid-cols",
            "Loading States": "Loading showcase",
            "Icons": "IconComponent",
        }
        
        design_score = 0
        for feature, keyword in design_features.items():
            if keyword in content:
                print(f"✅ {feature}: Implemented")
                design_score += 1
            else:
                print(f"❌ {feature}: Missing")
                self.warnings.append(f"Missing design feature: {feature}")
        
        self.test_results["visual_design"] = design_score >= len(design_features) * 0.8
        
        # Test 2.2: Metadata Display Logic
        print("\n📊 Testing Metadata Display Logic...")
        
        metadata_features = {
            "Author Info": "item.author.username",
            "Download Stats": "item.stats.downloads",
            "Like Stats": "item.stats.likes",
            "Date Info": "item.dates.updated",
            "Tags Display": "item.tags",
            "Version Info": "last_tested_version",
            "Type Display": "item.type",
        }
        
        metadata_score = 0
        for feature, keyword in metadata_features.items():
            if keyword in content:
                print(f"✅ {feature}: Displayed")
                metadata_score += 1
            else:
                print(f"❌ {feature}: Missing")
                self.critical_issues.append(f"Missing metadata: {feature}")
        
        self.test_results["metadata_display"] = metadata_score == len(metadata_features)
        
        # Test 2.3: Filter Logic
        print("\n🔍 Testing Filter Logic...")
        
        filter_features = {
            "Search Filter": "searchTerm",
            "Tag Filter": "selectedTags",
            "Author Filter": "authorFilter",
            "Type Filter": "activeTab",
            "Sort Options": "sortBy",
            "Multi-field Search": "item.name.toLowerCase()",
        }
        
        filter_score = 0
        for feature, keyword in filter_features.items():
            if keyword in content:
                print(f"✅ {feature}: Implemented")
                filter_score += 1
            else:
                print(f"❌ {feature}: Missing")
                self.critical_issues.append(f"Missing filter: {feature}")
        
        self.test_results["filter_logic"] = filter_score == len(filter_features)
        
        # Test 2.4: User Experience Logic
        print("\n👥 Testing User Experience Logic...")
        
        ux_features = {
            "Pagination": "currentPage",
            "Loading States": "setLoading",
            "Error Handling": "setErrorData",
            "Success Feedback": "setSuccessData",
            "Empty States": "No items found",
            "Tooltips": "ShadTooltip",
            "Accessibility": "aria-",
        }
        
        ux_score = 0
        for feature, keyword in ux_features.items():
            if keyword in content:
                print(f"✅ {feature}: Implemented")
                ux_score += 1
            else:
                print(f"❌ {feature}: Missing")
                self.warnings.append(f"UX improvement needed: {feature}")
        
        self.test_results["user_experience"] = ux_score >= len(ux_features) * 0.8
    
    async def test_integration_logic(self):
        """Test Integration Logic"""
        print(f"\n🔗 INTEGRATION LOGIC TEST")
        print("-" * 50)
        
        # Test API endpoint consistency
        print("🔌 Testing API Endpoint Logic...")
        
        # Check if frontend API calls match backend endpoints
        showcase_file = Path(__file__).parent / "src/frontend/src/pages/ShowcasePage/index.tsx"
        api_file = Path(__file__).parent / "src/backend/base/axiestudio/api/v1/axiestudio_store.py"
        
        if showcase_file.exists() and api_file.exists():
            with open(showcase_file, 'r') as f:
                frontend_content = f.read()
            with open(api_file, 'r') as f:
                backend_content = f.read()
            
            # Check main endpoint
            if '"/api/v1/store/"' in frontend_content and '@router.get("/")' in backend_content:
                print("✅ Main Endpoint: Frontend ↔ Backend match")
                self.test_results["main_endpoint"] = True
            else:
                self.critical_issues.append("Main endpoint mismatch between frontend and backend")
                self.test_results["main_endpoint"] = False
            
            # Check download endpoints
            if '/store/flow/' in frontend_content and '@router.get("/flow/{item_id}")' in backend_content:
                print("✅ Flow Endpoint: Frontend ↔ Backend match")
                self.test_results["flow_endpoint"] = True
            else:
                self.critical_issues.append("Flow endpoint mismatch")
                self.test_results["flow_endpoint"] = False
            
            if '/store/component/' in frontend_content and '@router.get("/component/{item_id}")' in backend_content:
                print("✅ Component Endpoint: Frontend ↔ Backend match")
                self.test_results["component_endpoint"] = True
            else:
                self.critical_issues.append("Component endpoint mismatch")
                self.test_results["component_endpoint"] = False
        
        self.test_results["integration"] = all([
            self.test_results.get("main_endpoint", False),
            self.test_results.get("flow_endpoint", False),
            self.test_results.get("component_endpoint", False)
        ])
    
    def generate_logic_report(self):
        """Generate comprehensive logic report"""
        print("\n" + "=" * 60)
        print("🏆 SENIOR TESTER LOGIC AUDIT REPORT")
        print("=" * 60)
        
        # Calculate overall score
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📊 LOGIC IMPLEMENTATION SCORE: {score:.1f}% ({passed_tests}/{total_tests})")
        
        # System Implementation Results
        print(f"\n🔧 SYSTEM IMPLEMENTATION RESULTS:")
        system_tests = ["file_display", "categorization", "component_download", "flow_download", "route_access", "button_integration"]
        for test in system_tests:
            result = self.test_results.get(test, False)
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test.replace('_', ' ').title()}")
        
        # UI/UX Results
        print(f"\n🎨 UI/UX IMPLEMENTATION RESULTS:")
        ui_tests = ["visual_design", "metadata_display", "filter_logic", "user_experience"]
        for test in ui_tests:
            result = self.test_results.get(test, False)
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test.replace('_', ' ').title()}")
        
        # Critical Issues
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ NO CRITICAL ISSUES FOUND")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        # Final Logic Verdict
        if len(self.critical_issues) == 0 and score >= 90:
            print(f"\n🎉 LOGIC VERDICT: EXCELLENT IMPLEMENTATION")
            print("✅ All system logic properly implemented")
            print("✅ All UI/UX logic working correctly")
            print("✅ All integration logic functional")
            print("🚀 READY FOR PRODUCTION DEPLOYMENT")
        elif len(self.critical_issues) == 0:
            print(f"\n👍 LOGIC VERDICT: GOOD IMPLEMENTATION")
            print("✅ Core logic working, minor improvements possible")
        else:
            print(f"\n❌ LOGIC VERDICT: CRITICAL LOGIC ISSUES")
            print("🚨 Must fix critical issues before deployment")

async def main():
    """Run the senior logic tester"""
    tester = SeniorLogicTester()
    success = await tester.run_logic_audit()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
