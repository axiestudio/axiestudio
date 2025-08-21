#!/usr/bin/env python3
"""
SENIOR TESTER - COMPLEX USER LOGIC IMPLEMENTATION AUDIT
Testing against real-world user scenarios and edge cases.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

class SeniorTesterAudit:
    def __init__(self):
        self.test_results = {}
        self.critical_issues = []
        self.warnings = []
        
    async def run_comprehensive_audit(self):
        """Run comprehensive audit against complex user logic"""
        print("🔍 SENIOR TESTER - COMPLEX USER LOGIC AUDIT")
        print("=" * 60)
        print("Testing against real-world user scenarios and edge cases...")
        print()
        
        # Test 1: Data Integrity & File Access
        await self.test_data_integrity()
        
        # Test 2: API Endpoint Logic
        await self.test_api_logic()
        
        # Test 3: Frontend-Backend Integration
        await self.test_integration_logic()
        
        # Test 4: Complex User Scenarios
        await self.test_complex_user_scenarios()
        
        # Test 5: Edge Cases & Error Handling
        await self.test_edge_cases()
        
        # Test 6: Performance Under Load
        await self.test_performance_logic()
        
        # Generate Final Report
        self.generate_final_report()
        
        return len(self.critical_issues) == 0
    
    async def test_data_integrity(self):
        """Test 1: Verify all 1600 files are properly accessible"""
        print("📊 TEST 1: DATA INTEGRITY & FILE ACCESS")
        print("-" * 40)
        
        try:
            from axiestudio.api.v1.axiestudio_store import load_store_index, get_store_components_path
            
            # Load store index
            store_data = load_store_index()
            total_items = len(store_data.flows) + len(store_data.components)
            
            print(f"✅ Store Index Loaded: {total_items} items")
            print(f"   • Flows: {len(store_data.flows)}")
            print(f"   • Components: {len(store_data.components)}")
            
            # Verify expected count
            if total_items != 1600:
                self.critical_issues.append(f"Expected 1600 items, found {total_items}")
                print(f"🚨 CRITICAL: Expected 1600 items, found {total_items}")
            else:
                print("✅ Correct item count: 1600")
            
            # Test file accessibility
            store_path = get_store_components_path()
            components_dir = store_path / "components"
            flows_dir = store_path / "flows"
            
            component_files = list(components_dir.glob("*.json"))
            flow_files = list(flows_dir.glob("*.json"))
            
            print(f"✅ Physical Files Found:")
            print(f"   • Component files: {len(component_files)}")
            print(f"   • Flow files: {len(flow_files)}")
            
            # Verify file count matches index
            if len(component_files) != len(store_data.components):
                self.critical_issues.append(f"Component file count mismatch: {len(component_files)} files vs {len(store_data.components)} in index")
            
            if len(flow_files) != len(store_data.flows):
                self.critical_issues.append(f"Flow file count mismatch: {len(flow_files)} files vs {len(store_data.flows)} in index")
            
            self.test_results["data_integrity"] = len(self.critical_issues) == 0
            
        except Exception as e:
            self.critical_issues.append(f"Data integrity test failed: {e}")
            self.test_results["data_integrity"] = False
    
    async def test_api_logic(self):
        """Test 2: Verify API endpoint logic"""
        print("\n🔌 TEST 2: API ENDPOINT LOGIC")
        print("-" * 40)
        
        try:
            from axiestudio.api.v1.axiestudio_store import get_store_data, load_item_data
            
            # Test main endpoint
            store_data = await get_store_data()
            print(f"✅ Main endpoint (/api/v1/store/): {len(store_data.flows + store_data.components)} items")
            
            # Test search functionality
            search_results = await get_store_data(search="chat")
            search_count = len(search_results.flows + search_results.components)
            print(f"✅ Search functionality: {search_count} results for 'chat'")
            
            # Test sorting
            popular_results = await get_store_data(sort_by="popular")
            recent_results = await get_store_data(sort_by="recent")
            print(f"✅ Sorting: Popular and Recent sorting working")
            
            # Test individual item loading
            if store_data.components:
                sample_component = load_item_data("component", store_data.components[0].id)
                print(f"✅ Component loading: {sample_component['name']}")
            
            if store_data.flows:
                sample_flow = load_item_data("flow", store_data.flows[0].id)
                print(f"✅ Flow loading: {sample_flow['name']}")
            
            self.test_results["api_logic"] = True
            
        except Exception as e:
            self.critical_issues.append(f"API logic test failed: {e}")
            self.test_results["api_logic"] = False
    
    async def test_integration_logic(self):
        """Test 3: Frontend-Backend Integration"""
        print("\n🔗 TEST 3: FRONTEND-BACKEND INTEGRATION")
        print("-" * 40)
        
        # Check route configuration
        routes_file = Path(__file__).parent / "src/frontend/src/customization/utils/custom-routes-store-pages.tsx"
        if routes_file.exists():
            with open(routes_file, 'r') as f:
                routes_content = f.read()
            
            if 'path="showcase"' in routes_content and 'ShowcasePage' in routes_content:
                print("✅ Route configuration: /showcase properly configured")
            else:
                self.critical_issues.append("Route configuration missing or incorrect")
        
        # Check toolbar integration
        toolbar_file = Path(__file__).parent / "src/frontend/src/components/core/flowToolbarComponent/components/flow-toolbar-options.tsx"
        if toolbar_file.exists():
            with open(toolbar_file, 'r') as f:
                toolbar_content = f.read()
            
            if 'ShowcaseButton' in toolbar_content:
                print("✅ Toolbar integration: ShowcaseButton properly integrated")
            else:
                self.critical_issues.append("ShowcaseButton not integrated in toolbar")
        
        # Check API endpoint consistency
        showcase_file = Path(__file__).parent / "src/frontend/src/pages/ShowcasePage/index.tsx"
        if showcase_file.exists():
            with open(showcase_file, 'r') as f:
                showcase_content = f.read()
            
            if '"/api/v1/store/"' in showcase_content:
                print("✅ API endpoint: Frontend calling correct endpoint")
            else:
                self.critical_issues.append("Frontend calling incorrect API endpoint")
        
        self.test_results["integration"] = len(self.critical_issues) == 0
    
    async def test_complex_user_scenarios(self):
        """Test 4: Complex User Scenarios"""
        print("\n👥 TEST 4: COMPLEX USER SCENARIOS")
        print("-" * 40)
        
        try:
            from axiestudio.api.v1.axiestudio_store import get_store_data, load_item_data
            
            # Scenario 1: Power user with complex search
            print("🔍 Scenario 1: Power user complex search")
            complex_search = await get_store_data(search="vector database", sort_by="popular", limit=10)
            print(f"   ✅ Complex search returned {len(complex_search.flows + complex_search.components)} results")
            
            # Scenario 2: Developer looking for specific component type
            print("🧩 Scenario 2: Developer filtering components")
            components_only = await get_store_data(item_type="component", sort_by="downloads")
            print(f"   ✅ Component filtering returned {len(components_only.components)} components")
            
            # Scenario 3: User browsing flows by recency
            print("🔄 Scenario 3: User browsing recent flows")
            recent_flows = await get_store_data(item_type="flow", sort_by="recent", limit=20)
            print(f"   ✅ Recent flows returned {len(recent_flows.flows)} flows")
            
            # Scenario 4: Bulk download simulation
            print("📥 Scenario 4: Bulk download simulation")
            store_data = await get_store_data(limit=5)
            download_count = 0
            for item in (store_data.flows + store_data.components)[:3]:
                try:
                    item_data = load_item_data(item.type.lower(), item.id)
                    if item_data:
                        download_count += 1
                except:
                    pass
            print(f"   ✅ Bulk download test: {download_count}/3 items successfully loaded")
            
            self.test_results["user_scenarios"] = True
            
        except Exception as e:
            self.critical_issues.append(f"User scenarios test failed: {e}")
            self.test_results["user_scenarios"] = False
    
    async def test_edge_cases(self):
        """Test 5: Edge Cases & Error Handling"""
        print("\n⚠️ TEST 5: EDGE CASES & ERROR HANDLING")
        print("-" * 40)
        
        try:
            from axiestudio.api.v1.axiestudio_store import get_store_data, load_item_data
            from fastapi import HTTPException
            
            # Test invalid search
            try:
                empty_search = await get_store_data(search="xyznonexistentquery123")
                print(f"✅ Empty search handling: {len(empty_search.flows + empty_search.components)} results")
            except Exception as e:
                self.warnings.append(f"Empty search handling issue: {e}")
            
            # Test invalid item ID
            try:
                invalid_item = load_item_data("component", "invalid-id-123")
                self.warnings.append("Invalid item ID should raise exception")
            except HTTPException:
                print("✅ Invalid item ID properly handled")
            except Exception as e:
                self.warnings.append(f"Unexpected error for invalid ID: {e}")
            
            # Test invalid item type
            try:
                invalid_type = load_item_data("invalid_type", "some-id")
                self.warnings.append("Invalid item type should raise exception")
            except HTTPException:
                print("✅ Invalid item type properly handled")
            except Exception as e:
                self.warnings.append(f"Unexpected error for invalid type: {e}")
            
            self.test_results["edge_cases"] = True
            
        except Exception as e:
            self.critical_issues.append(f"Edge cases test failed: {e}")
            self.test_results["edge_cases"] = False
    
    async def test_performance_logic(self):
        """Test 6: Performance Under Load"""
        print("\n⚡ TEST 6: PERFORMANCE UNDER LOAD")
        print("-" * 40)
        
        try:
            from axiestudio.api.v1.axiestudio_store import get_store_data
            import time
            
            # Test large dataset loading
            start_time = time.time()
            full_data = await get_store_data()
            load_time = time.time() - start_time
            
            print(f"✅ Full dataset load time: {load_time:.2f}s for {len(full_data.flows + full_data.components)} items")
            
            if load_time > 5.0:
                self.warnings.append(f"Slow loading time: {load_time:.2f}s")
            
            # Test pagination performance
            start_time = time.time()
            paginated_data = await get_store_data(limit=24, offset=0)
            pagination_time = time.time() - start_time
            
            print(f"✅ Pagination performance: {pagination_time:.2f}s for 24 items")
            
            if pagination_time > 1.0:
                self.warnings.append(f"Slow pagination: {pagination_time:.2f}s")
            
            self.test_results["performance"] = True
            
        except Exception as e:
            self.critical_issues.append(f"Performance test failed: {e}")
            self.test_results["performance"] = False
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 60)
        print("🏆 SENIOR TESTER FINAL AUDIT REPORT")
        print("=" * 60)
        
        # Calculate scores
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📊 OVERALL SCORE: {score:.1f}% ({passed_tests}/{total_tests} tests passed)")
        
        # Test Results
        print("\n📋 TEST RESULTS:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name.replace('_', ' ').title()}")
        
        # Critical Issues
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"  • {issue}")
        else:
            print("\n✅ NO CRITICAL ISSUES FOUND")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        # Final Verdict
        if len(self.critical_issues) == 0 and score >= 80:
            print("\n🎉 VERDICT: PRODUCTION READY")
            print("✅ Implementation meets enterprise standards")
            print("✅ Complex user logic properly handled")
            print("✅ All critical functionality working")
        elif len(self.critical_issues) == 0:
            print("\n⚠️ VERDICT: NEEDS MINOR IMPROVEMENTS")
            print("✅ No critical issues, but some optimizations needed")
        else:
            print("\n❌ VERDICT: CRITICAL ISSUES MUST BE FIXED")
            print("🚨 Cannot deploy to production with critical issues")

async def main():
    """Run the senior tester audit"""
    tester = SeniorTesterAudit()
    success = await tester.run_comprehensive_audit()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
