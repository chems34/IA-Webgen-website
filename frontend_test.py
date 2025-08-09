#!/usr/bin/env python3
"""
Frontend UI Testing for IA WebGen Pro
Comprehensive testing of all UI functionality using Playwright
"""

import asyncio
import sys
from playwright.async_api import async_playwright

class IAWebGenUITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.browser = None
        self.page = None

    async def setup(self):
        """Setup browser and page"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Enable console logging
        self.page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

    async def teardown(self):
        """Cleanup browser"""
        if self.browser:
            await self.browser.close()

    async def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = await test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
            else:
                print(f"❌ Failed")
            return success
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    async def test_page_loading(self):
        """Test basic page loading"""
        await self.page.goto('http://localhost:8000', wait_until='domcontentloaded', timeout=10000)
        
        # Check title
        title = await self.page.title()
        if "IA WebGen" not in title:
            return False
            
        # Check main elements
        main_title = await self.page.query_selector('h1')
        if not main_title:
            return False
            
        title_text = await main_title.inner_text()
        return "IA WebGen Pro" in title_text

    async def test_form_submission(self):
        """Test form filling and submission"""
        # Fill form fields
        await self.page.fill("#businessName", "Restaurant Le Gourmet")
        await self.page.select_option("#siteType", "restaurant")
        await self.page.fill("#description", "Un restaurant gastronomique français proposant une cuisine raffinée avec des produits locaux et de saison.")
        await self.page.fill("#userEmail", "contact@legourmet.fr")
        await self.page.fill("#phone", "01 23 45 67 89")
        await self.page.fill("#address", "123 Rue de la Gastronomie, 75001 Paris")
        await self.page.fill("#slogan", "L'art de la gastronomie française")
        
        # Submit form
        await self.page.click("button[type='submit']")
        
        # Wait for templates section to appear
        await self.page.wait_for_function(
            "document.getElementById('qualityTemplates').style.display !== 'none'",
            timeout=10000
        )
        
        # Check if templates are loaded
        template_cards = await self.page.query_selector_all(".template-card")
        return len(template_cards) > 0

    async def test_template_selection(self):
        """Test template selection and preview generation"""
        # Select first template
        template_cards = await self.page.query_selector_all(".template-card")
        if len(template_cards) == 0:
            return False
            
        await template_cards[0].click()
        
        # Check if continue button is enabled
        continue_btn = await self.page.wait_for_selector("#continueBtn:not([disabled])", timeout=5000)
        if not continue_btn:
            return False
            
        # Click continue to generate preview
        await continue_btn.click()
        
        # Wait for preview section
        await self.page.wait_for_function(
            "document.getElementById('previewSection').style.display !== 'none'",
            timeout=10000
        )
        
        # Check if preview content is generated
        preview_content = await self.page.inner_html("#websitePreview")
        return len(preview_content) > 100

    async def test_page_navigation(self):
        """Test navigation between generated pages"""
        # Check if page tabs exist
        page_tabs = await self.page.query_selector_all(".page-tab")
        if len(page_tabs) < 2:
            return False
            
        # Click on different tabs
        for i, tab in enumerate(page_tabs[:3]):  # Test first 3 tabs
            await tab.click()
            await self.page.wait_for_timeout(500)  # Wait for content to load
            
            # Check if tab is active
            classes = await tab.get_attribute("class")
            if "active" not in classes:
                return False
                
        return True

    async def test_edit_mode(self):
        """Test edit mode functionality"""
        # Find and click edit mode button
        edit_btn = await self.page.query_selector("#editModeBtn")
        if not edit_btn:
            return False
            
        await edit_btn.click()
        await self.page.wait_for_timeout(1000)
        
        # Check if edit mode is activated
        body_classes = await self.page.get_attribute("body", "class")
        if not body_classes or "edit-mode" not in body_classes:
            # Check if edit mode class is added to preview container
            preview_classes = await self.page.get_attribute("#websitePreview", "class")
            if not preview_classes or "edit-mode" not in preview_classes:
                return False
        
        # Check if editable elements have dotted borders
        editable_elements = await self.page.query_selector_all(".editable")
        return len(editable_elements) > 0

    async def test_chatgpt_widget(self):
        """Test ChatGPT widget functionality"""
        # Find and click ChatGPT toggle button
        chatgpt_toggle = await self.page.query_selector("#chatgptToggle")
        if not chatgpt_toggle:
            return False
            
        await chatgpt_toggle.click()
        await self.page.wait_for_timeout(1000)
        
        # Check if ChatGPT widget is visible
        chatgpt_widget = await self.page.query_selector("#miniChatGPT")
        if not chatgpt_widget:
            return False
            
        # Check if widget is displayed
        display_style = await chatgpt_widget.evaluate("el => getComputedStyle(el).display")
        if display_style == "none":
            return False
            
        # Test sending a message
        chat_input = await self.page.query_selector("#chatgptInput")
        if not chat_input:
            return False
            
        await chat_input.fill("aide")
        
        # Find and click send button
        send_btn = await self.page.query_selector("button:has-text('Envoyer')")
        if send_btn:
            await send_btn.click()
            await self.page.wait_for_timeout(1000)
            
        return True

    async def test_chatgpt_image_command(self):
        """Test ChatGPT image search command"""
        # Make sure ChatGPT is open
        chatgpt_widget = await self.page.query_selector("#miniChatGPT")
        if not chatgpt_widget:
            return False
            
        display_style = await chatgpt_widget.evaluate("el => getComputedStyle(el).display")
        if display_style == "none":
            # Open ChatGPT first
            chatgpt_toggle = await self.page.query_selector("#chatgptToggle")
            await chatgpt_toggle.click()
            await self.page.wait_for_timeout(1000)
        
        # Test image command
        chat_input = await self.page.query_selector("#chatgptInput")
        if not chat_input:
            return False
            
        await chat_input.fill("/image restaurant")
        
        send_btn = await self.page.query_selector("button:has-text('Envoyer')")
        if send_btn:
            await send_btn.click()
            await self.page.wait_for_timeout(2000)  # Wait longer for image search
            
        return True

    async def test_customization_options(self):
        """Test customization options in preview"""
        # Test color picker
        primary_color = await self.page.query_selector("#primaryColor")
        if primary_color:
            await primary_color.fill("#ff0000")
            
        secondary_color = await self.page.query_selector("#secondaryColor")
        if secondary_color:
            await secondary_color.fill("#00ff00")
            
        # Test title and subtitle changes
        main_title = await self.page.query_selector("#mainTitle")
        if main_title:
            await main_title.fill("Nouveau Titre")
            
        subtitle = await self.page.query_selector("#subtitle")
        if subtitle:
            await subtitle.fill("Nouveau sous-titre")
            
        # Click update preview button
        update_btn = await self.page.query_selector("button:has-text('Mettre à jour')")
        if update_btn:
            await update_btn.click()
            await self.page.wait_for_timeout(1000)
            
        return True

    async def test_finalization_flow(self):
        """Test the finalization and email flow"""
        # Find and click finalize button
        finalize_btn = await self.page.query_selector("button:has-text('RECEVOIR MON SITE PAR EMAIL')")
        if not finalize_btn:
            return False
            
        await finalize_btn.click()
        
        # Wait for email section
        await self.page.wait_for_function(
            "document.getElementById('emailSection').style.display !== 'none'",
            timeout=10000
        )
        
        # Check if email form is present
        email_form = await self.page.query_selector("#finalEmailForm")
        return email_form is not None

    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 IA WebGen Pro - Frontend UI Testing Started")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Phase 1: Basic Flow
            print("\n=== PHASE 1: BASIC FLOW ===")
            await self.run_test("Page Loading", self.test_page_loading)
            await self.run_test("Form Submission", self.test_form_submission)
            await self.run_test("Template Selection", self.test_template_selection)
            await self.run_test("Page Navigation", self.test_page_navigation)
            
            # Phase 2: Edit Mode
            print("\n=== PHASE 2: EDIT MODE ===")
            await self.run_test("Edit Mode Activation", self.test_edit_mode)
            await self.run_test("Customization Options", self.test_customization_options)
            
            # Phase 3: ChatGPT Widget
            print("\n=== PHASE 3: CHATGPT WIDGET ===")
            await self.run_test("ChatGPT Widget", self.test_chatgpt_widget)
            await self.run_test("ChatGPT Image Command", self.test_chatgpt_image_command)
            
            # Phase 4: Finalization
            print("\n=== PHASE 4: FINALIZATION ===")
            await self.run_test("Finalization Flow", self.test_finalization_flow)
            
        finally:
            await self.teardown()
        
        # Print results
        print("\n" + "=" * 60)
        print(f"📊 Tests Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("✅ All frontend tests passed! Application is working correctly.")
            return 0
        else:
            print("❌ Some frontend tests failed. Check the issues above.")
            return 1

async def main():
    tester = IAWebGenUITester()
    return await tester.run_all_tests()

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)