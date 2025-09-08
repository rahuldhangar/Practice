#!/usr/bin/env python3
"""
PIB Quick Test - Extract First 10 Pages
======================================

Quick test version to verify pagination works for multiple pages.

Author: AI Assistant
Version: 1.5 (Quick Test)
Date: September 2025
"""

import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from datetime import datetime

class PIBQuickTest:
    def __init__(self, headless=False, max_pages=10):
        """Initialize quick test extractor"""
        self.base_url = "https://accreditation.pib.gov.in/acridexsrch.aspx"
        self.all_data = []
        self.current_page = 1
        self.max_pages = max_pages
        self.headless = headless
        self.driver = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'pib_quick_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        logging.info("Chrome WebDriver initialized")
        
    def extract_data_from_page(self):
        """Extract data from current page"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                return []
                
            rows = tables[0].find_all('tr')
            page_data = []
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if cells:
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if any(row_data):  # Skip empty rows
                        page_data.append(row_data)
                        
            logging.info(f"Extracted {len(page_data)} records from page {self.current_page}")
            return page_data
            
        except Exception as e:
            logging.error(f"Error extracting data: {e}")
            return []
            
    def get_pagination_info(self):
        """Get pagination information"""
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            pagination_text = soup.find(string=re.compile(r'Page \d+ of \d+'))
            
            if pagination_text:
                match = re.search(r'Page (\d+) of (\d+)', pagination_text)
                if match:
                    return int(match.group(1)), int(match.group(2))
                    
            return None, None
            
        except Exception as e:
            logging.error(f"Error getting pagination: {e}")
            return None, None
            
    def navigate_to_next_page(self):
        """Navigate to next page"""
        try:
            next_elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Next")
            if not next_elements:
                next_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'lbNext')]")
                
            if next_elements:
                old_page, _ = self.get_pagination_info()
                
                self.driver.execute_script("arguments[0].click();", next_elements[0])
                time.sleep(3)  # Wait for navigation
                
                new_page, _ = self.get_pagination_info()
                if new_page and new_page > old_page:
                    self.current_page = new_page
                    logging.info(f"✅ Navigated to page {new_page}")
                    return True
                    
            return False
            
        except Exception as e:
            logging.error(f"Navigation error: {e}")
            return False
            
    def run_test(self):
        """Run the quick test"""
        try:
            print("="*60)
            print(f"PIB Quick Test - Extracting {self.max_pages} pages")
            print("="*60)
            
            self.setup_driver()
            
            # Load first page
            self.driver.get(self.base_url)
            
            # Get total pages info
            _, total_pages = self.get_pagination_info()
            if total_pages:
                print(f"Total pages available: {total_pages}")
            
            pages_processed = 0
            
            while pages_processed < self.max_pages:
                print(f"\n📄 Processing page {self.current_page}")
                
                # Extract data
                page_data = self.extract_data_from_page()
                
                if page_data:
                    self.all_data.extend(page_data)
                    print(f"   ✅ Extracted {len(page_data)} records")
                    print(f"   📊 Total records so far: {len(self.all_data)}")
                
                pages_processed += 1
                
                # Navigate to next page if not the last
                if pages_processed < self.max_pages:
                    if not self.navigate_to_next_page():
                        print("   ❌ Failed to navigate to next page")
                        break
                        
                time.sleep(2)  # Delay between pages
            
            # Save results
            if self.all_data:
                filename = f"PIB_Quick_Test_{self.max_pages}pages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df = pd.DataFrame(self.all_data)
                df.to_excel(filename, index=False)
                
                print("\n" + "="*60)
                print("🎉 QUICK TEST COMPLETED!")
                print(f"📊 Total records: {len(self.all_data)}")
                print(f"📄 Pages processed: {pages_processed}")
                print(f"💾 Data saved to: {filename}")
                print("="*60)
                
                # Show sample data
                if len(df) > 0:
                    print("\n📋 Sample data (first 5 rows):")
                    print(df.head())
                
                return True
            else:
                print("❌ No data extracted")
                return False
                
        except Exception as e:
            logging.error(f"Test failed: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

def main():
    """Main function for quick test"""
    # Test with 10 pages, visible browser
    tester = PIBQuickTest(headless=False, max_pages=10)
    return tester.run_test()

if __name__ == "__main__":
    main()