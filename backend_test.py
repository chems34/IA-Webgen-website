#!/usr/bin/env python3
"""
Backend Test for IA WebGen Pro
Since this is a static HTML application, we'll test the HTTP server functionality
"""

import requests
import sys
from datetime import datetime

class StaticSiteAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
            else:
                print(f"❌ Failed")
            return success
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_server_accessibility(self):
        """Test if the server is accessible"""
        response = requests.get(self.base_url, timeout=10)
        return response.status_code == 200

    def test_html_content(self):
        """Test if HTML content is properly served"""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            return False
        
        content = response.text
        # Check for key elements
        required_elements = [
            "IA WebGen Pro",
            "websiteForm",
            "businessName",
            "siteType", 
            "description",
            "userEmail"
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"Missing required element: {element}")
                return False
        
        return True

    def test_static_resources(self):
        """Test if external resources are referenced correctly"""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            return False
            
        content = response.text
        # Check for external CSS/JS references
        external_resources = [
            "tailwindcss",
            "font-awesome"
        ]
        
        for resource in external_resources:
            if resource not in content:
                print(f"Missing external resource reference: {resource}")
                return False
                
        return True

    def test_form_elements(self):
        """Test if all required form elements are present"""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            return False
            
        content = response.text
        form_elements = [
            'id="businessName"',
            'id="siteType"',
            'id="description"',
            'id="userEmail"',
            'id="phone"',
            'id="address"'
        ]
        
        for element in form_elements:
            if element not in content:
                print(f"Missing form element: {element}")
                return False
                
        return True

    def test_javascript_functionality(self):
        """Test if JavaScript functions are defined"""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            return False
            
        content = response.text
        js_functions = [
            "handleFormSubmit",
            "generateCompleteWebsite",
            "displayTemplates",
            "selectTemplate",
            "toggleEditMode",
            "toggleChatGPT"
        ]
        
        for func in js_functions:
            if func not in content:
                print(f"Missing JavaScript function: {func}")
                return False
                
        return True

    def test_css_styles(self):
        """Test if required CSS classes are defined"""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            return False
            
        content = response.text
        css_classes = [
            ".edit-mode",
            ".editable",
            ".mini-chatgpt",
            ".template-card",
            ".page-tab"
        ]
        
        for css_class in css_classes:
            if css_class not in content:
                print(f"Missing CSS class: {css_class}")
                return False
                
        return True

def main():
    print("🚀 IA WebGen Pro - Backend Testing Started")
    print("=" * 50)
    
    # Setup
    tester = StaticSiteAPITester("http://localhost:8000")
    
    # Run tests
    tests = [
        ("Server Accessibility", tester.test_server_accessibility),
        ("HTML Content Structure", tester.test_html_content),
        ("Static Resources References", tester.test_static_resources),
        ("Form Elements Presence", tester.test_form_elements),
        ("JavaScript Functions", tester.test_javascript_functionality),
        ("CSS Styles", tester.test_css_styles)
    ]
    
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Tests Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.tests_passed == tester.tests_run:
        print("✅ All backend tests passed! Static site is properly configured.")
        return 0
    else:
        print("❌ Some backend tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())