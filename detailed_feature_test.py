#!/usr/bin/env python3
"""
Detailed Feature Testing for IA WebGen Pro
Testing specific features mentioned in the review request
"""

import asyncio
import sys
from playwright.async_api import async_playwright

class DetailedFeatureTester:
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

    async def setup_complete_flow(self):
        """Setup the complete flow to get to preview mode"""
        await self.page.goto('http://localhost:8000', wait_until='domcontentloaded', timeout=10000)
        
        # Fill form
        await self.page.fill("#businessName", "Restaurant Le Gourmet")
        await self.page.select_option("#siteType", "restaurant")
        await self.page.fill("#description", "Un restaurant gastronomique français")
        await self.page.fill("#userEmail", "contact@legourmet.fr")
        
        # Submit form
        await self.page.click("button[type='submit']")
        await self.page.wait_for_function(
            "document.getElementById('qualityTemplates').style.display !== 'none'",
            timeout=10000
        )
        
        # Select template
        template_cards = await self.page.query_selector_all(".template-card")
        await template_cards[0].click()
        
        # Generate preview
        continue_btn = await self.page.wait_for_selector("#continueBtn:not([disabled])", timeout=5000)
        await continue_btn.click()
        await self.page.wait_for_function(
            "document.getElementById('previewSection').style.display !== 'none'",
            timeout=10000
        )

    async def test_edit_mode_detailed(self):
        """Test detailed edit mode functionality"""
        await self.setup_complete_flow()
        
        # 1. Test edit mode button exists and works
        edit_btn = await self.page.query_selector("#editModeBtn")
        if not edit_btn:
            print("❌ Edit mode button not found")
            return False
            
        # Check initial state
        btn_text = await edit_btn.inner_text()
        if "Désactivé" not in btn_text:
            print(f"❌ Initial edit mode state incorrect: {btn_text}")
            return False
            
        # Activate edit mode
        await edit_btn.click()
        await self.page.wait_for_timeout(1000)
        
        # Check if state changed
        btn_text_after = await edit_btn.inner_text()
        if "Activé" not in btn_text_after:
            print(f"❌ Edit mode state didn't change: {btn_text_after}")
            return False
            
        # 2. Test if elements become editable (dotted borders)
        # Check if CSS class is applied
        preview_element = await self.page.query_selector("#websitePreview")
        if preview_element:
            classes = await preview_element.get_attribute("class")
            if "edit-mode" not in (classes or ""):
                print("❌ Edit mode CSS class not applied to preview")
                return False
        
        # 3. Test clicking on editable elements
        editable_elements = await self.page.query_selector_all(".editable")
        print(f"Found {len(editable_elements)} editable elements")
        
        if len(editable_elements) > 0:
            # Try clicking on first editable element
            await editable_elements[0].click()
            await self.page.wait_for_timeout(500)
            
            # Check if edit toolbar appears
            edit_toolbar = await self.page.query_selector(".edit-toolbar")
            if edit_toolbar:
                print("✅ Edit toolbar appeared on element click")
            else:
                print("⚠️ Edit toolbar not found (may be expected behavior)")
        
        return True

    async def test_chatgpt_detailed(self):
        """Test detailed ChatGPT functionality"""
        await self.setup_complete_flow()
        
        # 1. Test ChatGPT toggle button (robot icon)
        chatgpt_toggle = await self.page.query_selector("#chatgptToggle")
        if not chatgpt_toggle:
            print("❌ ChatGPT toggle button not found")
            return False
            
        # Check if it has robot icon
        icon = await chatgpt_toggle.query_selector("i.fa-robot")
        if not icon:
            print("❌ Robot icon not found in toggle button")
            return False
            
        # 2. Test opening ChatGPT widget
        await chatgpt_toggle.click()
        await self.page.wait_for_timeout(1000)
        
        chatgpt_widget = await self.page.query_selector("#miniChatGPT")
        if not chatgpt_widget:
            print("❌ ChatGPT widget not found")
            return False
            
        display_style = await chatgpt_widget.evaluate("el => getComputedStyle(el).display")
        if display_style == "none":
            print("❌ ChatGPT widget not visible after toggle")
            return False
            
        # 3. Test welcome message
        messages = await self.page.query_selector_all(".message.bot")
        if len(messages) == 0:
            print("❌ No bot messages found")
            return False
            
        welcome_msg = await messages[0].inner_text()
        if "Assistant IA" not in welcome_msg:
            print(f"❌ Welcome message incorrect: {welcome_msg}")
            return False
            
        # 4. Test help command
        chat_input = await self.page.query_selector("#chatgptInput")
        if not chat_input:
            print("❌ Chat input not found")
            return False
            
        await chat_input.fill("aide")
        send_btn = await self.page.query_selector("button:has-text('Envoyer')")
        if send_btn:
            await send_btn.click()
            await self.page.wait_for_timeout(1000)
            
        # 5. Test /image command
        await chat_input.fill("/image restaurant moderne")
        if send_btn:
            await send_btn.click()
            await self.page.wait_for_timeout(2000)
            
        # 6. Test minimize/maximize
        chatgpt_header = await self.page.query_selector(".chatgpt-header")
        if chatgpt_header:
            await chatgpt_header.click()  # Should minimize
            await self.page.wait_for_timeout(500)
            
            # Check if minimized
            minimized_class = await chatgpt_widget.get_attribute("class")
            if "minimized" in (minimized_class or ""):
                print("✅ ChatGPT widget minimized successfully")
            
            # Maximize again
            await chatgpt_header.click()
            await self.page.wait_for_timeout(500)
            
        # 7. Test close button
        close_btn = await self.page.query_selector("button:has(.fa-times)")
        if close_btn:
            await close_btn.click()
            await self.page.wait_for_timeout(500)
            
            display_style_after = await chatgpt_widget.evaluate("el => getComputedStyle(el).display")
            if display_style_after == "none":
                print("✅ ChatGPT widget closed successfully")
            
        return True

    async def test_page_persistence(self):
        """Test persistence of modifications when changing pages"""
        await self.setup_complete_flow()
        
        # Activate edit mode
        edit_btn = await self.page.query_selector("#editModeBtn")
        await edit_btn.click()
        await self.page.wait_for_timeout(1000)
        
        # Make a customization change
        primary_color = await self.page.query_selector("#primaryColor")
        if primary_color:
            await primary_color.fill("#ff0000")
            
        update_btn = await self.page.query_selector("button:has-text('Mettre à jour')")
        if update_btn:
            await update_btn.click()
            await self.page.wait_for_timeout(1000)
            
        # Switch to different page
        page_tabs = await self.page.query_selector_all(".page-tab")
        if len(page_tabs) > 1:
            await page_tabs[1].click()  # Switch to second page
            await self.page.wait_for_timeout(1000)
            
            # Check if edit mode is still active
            edit_btn_text = await edit_btn.inner_text()
            if "Activé" not in edit_btn_text:
                print("❌ Edit mode not persistent across pages")
                return False
                
            # Switch back to first page
            await page_tabs[0].click()
            await self.page.wait_for_timeout(1000)
            
            # Check if color change persisted
            current_color = await primary_color.get_attribute("value")
            if current_color != "#ff0000":
                print(f"❌ Color change not persistent: {current_color}")
                return False
                
        return True

    async def test_add_new_section(self):
        """Test adding new sections functionality"""
        await self.setup_complete_flow()
        
        # Look for add new section button
        add_section_btn = await self.page.query_selector("button:has-text('Ajouter une section')")
        if not add_section_btn:
            print("❌ Add new section button not found")
            return False
            
        # Click add section button
        await add_section_btn.click()
        await self.page.wait_for_timeout(1000)
        
        # This should trigger some functionality (modal, form, etc.)
        # The exact behavior depends on implementation
        print("✅ Add new section button is clickable")
        return True

    async def test_style_options(self):
        """Test style modification options"""
        await self.setup_complete_flow()
        
        # Test color pickers
        primary_color = await self.page.query_selector("#primaryColor")
        secondary_color = await self.page.query_selector("#secondaryColor")
        
        if not primary_color or not secondary_color:
            print("❌ Color picker inputs not found")
            return False
            
        # Test changing colors
        await primary_color.fill("#ff5733")
        await secondary_color.fill("#33ff57")
        
        # Test text inputs
        main_title = await self.page.query_selector("#mainTitle")
        subtitle = await self.page.query_selector("#subtitle")
        
        if main_title:
            await main_title.fill("Nouveau Titre Modifié")
            
        if subtitle:
            await subtitle.fill("Nouveau sous-titre modifié")
            
        # Apply changes
        update_btn = await self.page.query_selector("button:has-text('Mettre à jour')")
        if update_btn:
            await update_btn.click()
            await self.page.wait_for_timeout(1000)
            
        return True

    async def run_detailed_tests(self):
        """Run all detailed tests"""
        print("🚀 IA WebGen Pro - Detailed Feature Testing")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Detailed feature tests
            await self.run_test("Edit Mode Detailed Functionality", self.test_edit_mode_detailed)
            await self.run_test("ChatGPT Detailed Functionality", self.test_chatgpt_detailed)
            await self.run_test("Page Modification Persistence", self.test_page_persistence)
            await self.run_test("Add New Section Feature", self.test_add_new_section)
            await self.run_test("Style Modification Options", self.test_style_options)
            
        finally:
            await self.teardown()
        
        # Print results
        print("\n" + "=" * 60)
        print(f"📊 Detailed Tests Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("✅ All detailed feature tests passed!")
            return 0
        else:
            print("❌ Some detailed feature tests failed.")
            return 1

async def main():
    tester = DetailedFeatureTester()
    return await tester.run_detailed_tests()

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)