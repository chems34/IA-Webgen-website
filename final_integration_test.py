#!/usr/bin/env python3
"""
Final Integration Test Report for IA WebGen Pro
Comprehensive testing summary and issue identification
"""

import asyncio
import sys
from playwright.async_api import async_playwright

class FinalIntegrationTester:
    def __init__(self):
        self.issues_found = []
        self.successes = []
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

    async def setup_complete_flow(self):
        """Setup the complete flow to get to preview mode"""
        await self.page.goto('http://localhost:8000', wait_until='domcontentloaded', timeout=10000)
        
        # Fill form
        await self.page.fill("#businessName", "Restaurant Le Gourmet")
        await self.page.select_option("#siteType", "restaurant")
        await self.page.fill("#description", "Un restaurant gastronomique français proposant une cuisine raffinée")
        await self.page.fill("#userEmail", "contact@legourmet.fr")
        await self.page.fill("#phone", "01 23 45 67 89")
        await self.page.fill("#address", "123 Rue de la Gastronomie, 75001 Paris")
        
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

    async def test_comprehensive_flow(self):
        """Test the complete user flow comprehensively"""
        print("🔍 Testing comprehensive user flow...")
        
        try:
            # Phase 1: Basic Flow
            print("\n=== PHASE 1: BASIC FLOW ===")
            await self.page.goto('http://localhost:8000', wait_until='domcontentloaded', timeout=10000)
            
            # Check page loading
            title = await self.page.title()
            if "IA WebGen" in title:
                self.successes.append("✅ Page loads correctly with proper title")
            else:
                self.issues_found.append("❌ Page title incorrect")
            
            # Test form submission
            await self.page.fill("#businessName", "Restaurant Le Gourmet")
            await self.page.select_option("#siteType", "restaurant")
            await self.page.fill("#description", "Un restaurant gastronomique français proposant une cuisine raffinée avec des produits locaux et de saison. Nous offrons une expérience culinaire unique dans un cadre élégant.")
            await self.page.fill("#userEmail", "contact@legourmet.fr")
            await self.page.fill("#phone", "01 23 45 67 89")
            await self.page.fill("#address", "123 Rue de la Gastronomie, 75001 Paris")
            await self.page.fill("#slogan", "L'art de la gastronomie française")
            
            # Check page selection checkboxes
            page_checkboxes = await self.page.query_selector_all('input[id^="page-"]:checked')
            if len(page_checkboxes) >= 3:
                self.successes.append(f"✅ {len(page_checkboxes)} pages selected by default")
            else:
                self.issues_found.append("❌ Insufficient default pages selected")
            
            await self.page.click("button[type='submit']")
            await self.page.wait_for_function(
                "document.getElementById('qualityTemplates').style.display !== 'none'",
                timeout=10000
            )
            self.successes.append("✅ Form submission navigates to templates correctly")
            
            # Test template selection
            template_cards = await self.page.query_selector_all(".template-card")
            if len(template_cards) >= 10:
                self.successes.append(f"✅ {len(template_cards)} templates available")
            else:
                self.issues_found.append(f"❌ Only {len(template_cards)} templates found, expected 10")
            
            await template_cards[0].click()
            continue_btn = await self.page.wait_for_selector("#continueBtn:not([disabled])", timeout=5000)
            await continue_btn.click()
            await self.page.wait_for_function(
                "document.getElementById('previewSection').style.display !== 'none'",
                timeout=10000
            )
            self.successes.append("✅ Template selection and preview generation works")
            
            # Phase 2: Edit Mode Testing
            print("\n=== PHASE 2: EDIT MODE TESTING ===")
            
            # Test edit mode button
            edit_btn = await self.page.query_selector("#editModeBtn")
            if edit_btn:
                btn_text = await edit_btn.inner_text()
                if "Désactivé" in btn_text:
                    self.successes.append("✅ Edit mode button found with correct initial state")
                else:
                    self.issues_found.append(f"❌ Edit mode button state incorrect: {btn_text}")
                
                # Activate edit mode
                await edit_btn.click()
                await self.page.wait_for_timeout(1000)
                
                btn_text_after = await edit_btn.inner_text()
                if "Activé" in btn_text_after:
                    self.successes.append("✅ Edit mode activates correctly")
                else:
                    self.issues_found.append(f"❌ Edit mode activation failed: {btn_text_after}")
                
                # Check for editable elements
                editable_elements = await self.page.query_selector_all(".editable")
                if len(editable_elements) > 0:
                    self.successes.append(f"✅ {len(editable_elements)} elements become editable")
                    
                    # Test clicking on editable element
                    await editable_elements[0].click()
                    await self.page.wait_for_timeout(500)
                    
                    # Check for edit toolbar
                    edit_toolbar = await self.page.query_selector(".edit-toolbar")
                    if edit_toolbar:
                        self.successes.append("✅ Edit toolbar appears on element click")
                    else:
                        self.issues_found.append("❌ Edit toolbar doesn't appear on element click")
                else:
                    self.issues_found.append("❌ No elements become editable in edit mode")
            else:
                self.issues_found.append("❌ Edit mode button not found")
            
            # Test customization options
            primary_color = await self.page.query_selector("#primaryColor")
            secondary_color = await self.page.query_selector("#secondaryColor")
            main_title = await self.page.query_selector("#mainTitle")
            subtitle = await self.page.query_selector("#subtitle")
            
            if all([primary_color, secondary_color, main_title, subtitle]):
                self.successes.append("✅ All customization controls found")
                
                # Test color changes
                await primary_color.fill("#ff5733")
                await secondary_color.fill("#33ff57")
                await main_title.fill("Nouveau Titre")
                await subtitle.fill("Nouveau Sous-titre")
                
                update_btn = await self.page.query_selector("button:has-text('Mettre à jour')")
                if update_btn:
                    await update_btn.click()
                    await self.page.wait_for_timeout(1000)
                    self.successes.append("✅ Customization updates work")
                else:
                    self.issues_found.append("❌ Update preview button not found")
            else:
                self.issues_found.append("❌ Some customization controls missing")
            
            # Test add new section
            add_section_btn = await self.page.query_selector("button:has-text('Ajouter une section')")
            if add_section_btn:
                await add_section_btn.click()
                await self.page.wait_for_timeout(1000)
                self.successes.append("✅ Add new section button works")
            else:
                self.issues_found.append("❌ Add new section button not found")
            
            # Phase 3: ChatGPT Testing
            print("\n=== PHASE 3: CHATGPT TESTING ===")
            
            # Test ChatGPT toggle
            chatgpt_toggle = await self.page.query_selector("#chatgptToggle")
            if chatgpt_toggle:
                # Check robot icon
                robot_icon = await chatgpt_toggle.query_selector("i.fa-robot")
                if robot_icon:
                    self.successes.append("✅ ChatGPT toggle button with robot icon found")
                else:
                    self.issues_found.append("❌ Robot icon missing from ChatGPT toggle")
                
                # Open ChatGPT
                await chatgpt_toggle.click()
                await self.page.wait_for_timeout(1000)
                
                chatgpt_widget = await self.page.query_selector("#miniChatGPT")
                if chatgpt_widget:
                    display_style = await chatgpt_widget.evaluate("el => getComputedStyle(el).display")
                    if display_style != "none":
                        self.successes.append("✅ ChatGPT widget opens correctly")
                        
                        # Test welcome message
                        bot_messages = await self.page.query_selector_all(".message.bot")
                        if len(bot_messages) > 0:
                            welcome_text = await bot_messages[0].inner_text()
                            if "Assistant IA" in welcome_text:
                                self.successes.append("✅ ChatGPT welcome message correct")
                            else:
                                self.issues_found.append("❌ ChatGPT welcome message incorrect")
                        
                        # Test chat input
                        chat_input = await self.page.query_selector("#chatgptInput")
                        if chat_input:
                            # Test help command
                            await chat_input.fill("aide")
                            send_btn = await self.page.query_selector("button:has-text('Envoyer')")
                            if send_btn:
                                await send_btn.click()
                                await self.page.wait_for_timeout(1000)
                                self.successes.append("✅ ChatGPT help command works")
                                
                                # Test /image command
                                await chat_input.fill("/image restaurant moderne")
                                await send_btn.click()
                                await self.page.wait_for_timeout(2000)
                                self.successes.append("✅ ChatGPT /image command works")
                            else:
                                self.issues_found.append("❌ ChatGPT send button not found")
                        else:
                            self.issues_found.append("❌ ChatGPT input field not found")
                        
                        # Test minimize/maximize
                        chatgpt_header = await self.page.query_selector(".chatgpt-header")
                        if chatgpt_header:
                            await chatgpt_header.click()  # Minimize
                            await self.page.wait_for_timeout(500)
                            
                            minimized_class = await chatgpt_widget.get_attribute("class")
                            if "minimized" in (minimized_class or ""):
                                self.successes.append("✅ ChatGPT minimizes correctly")
                            else:
                                self.issues_found.append("❌ ChatGPT minimize doesn't work")
                            
                            await chatgpt_header.click()  # Maximize
                            await self.page.wait_for_timeout(500)
                        
                        # Test close
                        close_btn = await self.page.query_selector("button:has(.fa-times)")
                        if close_btn:
                            await close_btn.click()
                            await self.page.wait_for_timeout(500)
                            
                            display_after = await chatgpt_widget.evaluate("el => getComputedStyle(el).display")
                            if display_after == "none":
                                self.successes.append("✅ ChatGPT closes correctly")
                            else:
                                self.issues_found.append("❌ ChatGPT close doesn't work")
                    else:
                        self.issues_found.append("❌ ChatGPT widget doesn't open")
                else:
                    self.issues_found.append("❌ ChatGPT widget not found")
            else:
                self.issues_found.append("❌ ChatGPT toggle button not found")
            
            # Phase 4: Navigation Testing
            print("\n=== PHASE 4: NAVIGATION TESTING ===")
            
            # Test page navigation
            page_tabs = await self.page.query_selector_all(".page-tab")
            if len(page_tabs) >= 3:
                self.successes.append(f"✅ {len(page_tabs)} page navigation tabs found")
                
                # Test clicking different tabs
                for i, tab in enumerate(page_tabs[:3]):
                    await tab.click()
                    await self.page.wait_for_timeout(500)
                    
                    classes = await tab.get_attribute("class")
                    if "active" in (classes or ""):
                        self.successes.append(f"✅ Page tab {i+1} activates correctly")
                    else:
                        self.issues_found.append(f"❌ Page tab {i+1} doesn't activate")
            else:
                self.issues_found.append("❌ Insufficient page navigation tabs")
            
            # Phase 5: Finalization Testing
            print("\n=== PHASE 5: FINALIZATION TESTING ===")
            
            finalize_btn = await self.page.query_selector("button:has-text('RECEVOIR MON SITE PAR EMAIL')")
            if finalize_btn:
                await finalize_btn.click()
                await self.page.wait_for_function(
                    "document.getElementById('emailSection').style.display !== 'none'",
                    timeout=10000
                )
                
                email_form = await self.page.query_selector("#finalEmailForm")
                if email_form:
                    self.successes.append("✅ Finalization flow works correctly")
                    
                    # Test email form
                    email_input = await self.page.query_selector("#deliveryEmail")
                    if email_input:
                        await email_input.fill("test@example.com")
                        
                        send_email_btn = await self.page.query_selector("button:has-text('ENVOYER MON SITE MAINTENANT')")
                        if send_email_btn:
                            self.successes.append("✅ Email delivery form complete")
                        else:
                            self.issues_found.append("❌ Send email button not found")
                    else:
                        self.issues_found.append("❌ Email input field not found")
                else:
                    self.issues_found.append("❌ Email form not found")
            else:
                self.issues_found.append("❌ Finalize button not found")
                
        except Exception as e:
            self.issues_found.append(f"❌ Critical error during testing: {str(e)}")

    async def run_final_test(self):
        """Run final comprehensive test"""
        print("🚀 IA WebGen Pro - Final Integration Test")
        print("=" * 70)
        
        await self.setup()
        
        try:
            await self.test_comprehensive_flow()
        finally:
            await self.teardown()
        
        # Generate report
        print("\n" + "=" * 70)
        print("📊 FINAL TEST REPORT")
        print("=" * 70)
        
        print(f"\n✅ SUCCESSES ({len(self.successes)}):")
        for success in self.successes:
            print(f"  {success}")
        
        print(f"\n❌ ISSUES FOUND ({len(self.issues_found)}):")
        for issue in self.issues_found:
            print(f"  {issue}")
        
        # Overall assessment
        total_tests = len(self.successes) + len(self.issues_found)
        success_rate = (len(self.successes) / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 OVERALL ASSESSMENT:")
        print(f"  Success Rate: {success_rate:.1f}% ({len(self.successes)}/{total_tests})")
        
        if success_rate >= 90:
            print("  🎉 EXCELLENT - Application is working very well!")
            return 0
        elif success_rate >= 75:
            print("  ✅ GOOD - Application is mostly functional with minor issues")
            return 0
        elif success_rate >= 50:
            print("  ⚠️ FAIR - Application has some significant issues")
            return 1
        else:
            print("  ❌ POOR - Application has major issues")
            return 1

async def main():
    tester = FinalIntegrationTester()
    return await tester.run_final_test()

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)