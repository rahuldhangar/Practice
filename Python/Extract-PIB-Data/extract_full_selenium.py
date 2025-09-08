#!/usr/bin/env python3
"""
PIB Accredited Media Persons - Full Data Extraction (Selenium)
==============================================================

Production version for extracting all 191 pages of PIB data efficiently.

Author: AI Assistant  
Version: 2.0 (Production)
Date: September 2025

Features:
- Extracts data from all 191 pages
- Progress tracking and resume capability  
- Enhanced error handling and retry logic
- Optimized performance with smart waits
- Detailed logging and monitoring
"""

import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime

class PIBFullExtractor:
    def __init__(self, headless=True, resume_from_page=1):
        """Initialize the PIB full data extractor"""
        self.base_url = "https://accreditation.pib.gov.in/acridexsrch.aspx"
        self.all_data = []
        self.current_page = resume_from_page
        self.total_pages = 191
        self.headless = headless
        self.driver = None
        
        # Performance settings
        self.page_load_timeout = 30
        self.element_wait_timeout = 10
        self.navigation_delay = 2
        
        # Progress tracking
        self.checkpoint_interval = 10  # Save progress every 10 pages
        self.checkpoint_file = "pib_extraction_progress.json"
        self.output_file = f"PIB_Accredited_Media_Persons_FULL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Setup logging
        self.setup_logging()
        
        # Load existing progress if available
        self.load_progress()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_filename = f"pib_full_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Setup optimized Chrome WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            
        # Performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Don't load images for faster performance
        chrome_options.add_argument("--disable-javascript")  # We don't need JS except for navigation
        chrome_options.add_argument("--window-size=1920,1080")
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Additional performance settings
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # Block images
            "profile.default_content_setting_values.notifications": 2,  # Block notifications
            "profile.default_content_settings.popups": 0,  # Block popups
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(self.page_load_timeout)
            self.logger.info("Optimized Chrome WebDriver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            raise
            
    def load_progress(self):
        """Load existing extraction progress"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    progress = json.load(f)
                    
                self.current_page = progress.get('current_page', 1)
                saved_data_file = progress.get('data_file')
                
                if saved_data_file and os.path.exists(saved_data_file):
                    # Load existing data
                    df = pd.read_excel(saved_data_file)
                    self.all_data = df.values.tolist()
                    self.logger.info(f"Resumed from page {self.current_page} with {len(self.all_data)} existing records")
                else:
                    self.logger.info(f"Starting fresh from page {self.current_page}")
                    
            except Exception as e:
                self.logger.error(f"Error loading progress: {e}. Starting fresh.")
                self.current_page = 1
                
    def save_progress(self):
        """Save current extraction progress"""
        try:
            # Save current data to temp file
            temp_file = f"temp_pib_data_{self.current_page}.xlsx"
            if self.all_data:
                df = pd.DataFrame(self.all_data)
                df.to_excel(temp_file, index=False)
                
            # Save progress info
            progress = {
                'current_page': self.current_page,
                'total_pages': self.total_pages,
                'records_extracted': len(self.all_data),
                'data_file': temp_file,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.checkpoint_file, 'w') as f:
                json.dump(progress, f, indent=2)
                
            self.logger.info(f"Progress saved: Page {self.current_page}, {len(self.all_data)} records")
            
        except Exception as e:
            self.logger.error(f"Error saving progress: {e}")
            
    def extract_data_from_page(self):
        """Extract data from current page with enhanced error handling"""
        try:
            # Wait for table to be present
            WebDriverWait(self.driver, self.element_wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # Get page source and parse
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find data table
            tables = soup.find_all('table')
            if not tables:
                self.logger.warning(f"No tables found on page {self.current_page}")
                return []
                
            main_table = tables[0]
            rows = main_table.find_all('tr')
            
            page_data = []
            headers_found = False
            
            for i, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                if not cells:
                    continue
                    
                row_data = []
                for cell in cells:
                    text = cell.get_text(strip=True)
                    row_data.append(text)
                
                # Skip empty rows
                if not any(row_data):
                    continue
                    
                # Detect header row
                if not headers_found and any('SL.No' in str(cell).upper() or 'NAME' in str(cell).upper() for cell in row_data):
                    headers_found = True
                    if self.current_page == 1:  # Only add headers from first page
                        page_data.append(row_data)
                    continue
                    
                # Add data rows
                if headers_found and len(row_data) >= 2:
                    page_data.append(row_data)
                    
            self.logger.info(f"Extracted {len(page_data)} records from page {self.current_page}")
            return page_data
            
        except TimeoutException:
            self.logger.error(f"Timeout waiting for page {self.current_page} to load")
            return []
        except Exception as e:
            self.logger.error(f"Error extracting data from page {self.current_page}: {e}")
            return []
            
    def get_pagination_info(self):
        """Get current pagination information"""
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            pagination_text = soup.find(string=re.compile(r'Page \d+ of \d+'))
            if pagination_text:
                match = re.search(r'Page (\d+) of (\d+)', pagination_text)
                if match:
                    current_page = int(match.group(1))
                    total_pages = int(match.group(2))
                    return current_page, total_pages
                    
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error getting pagination info: {e}")
            return None, None
            
    def navigate_to_next_page(self):
        """Navigate to next page with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Find next page link
                next_elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Next")
                if not next_elements:
                    next_elements = self.driver.find_elements(By.LINK_TEXT, ">")
                if not next_elements:
                    next_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'lbNext')]")
                    
                if not next_elements:
                    self.logger.info("No next page link found - reached last page")
                    return False
                    
                # Store current page for verification
                old_page, _ = self.get_pagination_info()
                
                # Click next link
                next_element = next_elements[0]
                self.driver.execute_script("arguments[0].click();", next_element)
                
                # Wait for navigation with timeout
                start_time = time.time()
                while time.time() - start_time < self.page_load_timeout:
                    time.sleep(1)
                    new_page, _ = self.get_pagination_info()
                    if new_page and new_page > old_page:
                        self.current_page = new_page
                        self.logger.info(f"✅ Successfully navigated to page {new_page}")
                        return True
                        
                self.logger.warning(f"Attempt {attempt + 1}: Page navigation failed")
                time.sleep(2)  # Wait before retry
                
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1}: Error navigating to next page: {e}")
                time.sleep(2)
                
        self.logger.error("Failed to navigate to next page after all retries")
        return False
        
    def extract_all_data(self):
        """Extract data from all pages with progress tracking"""
        try:
            self.logger.info("="*80)
            self.logger.info("Starting FULL PIB Accredited Media Persons data extraction")
            self.logger.info(f"Target: {self.total_pages} pages")
            self.logger.info(f"Resume from page: {self.current_page}")
            self.logger.info(f"Output file: {self.output_file}")
            self.logger.info("="*80)
            
            # Load first page
            if self.current_page == 1:
                self.driver.get(self.base_url)
                WebDriverWait(self.driver, self.page_load_timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Verify total pages
                _, total_pages = self.get_pagination_info()
                if total_pages:
                    self.total_pages = total_pages
                    self.logger.info(f"Confirmed total pages: {total_pages}")
            
            page_count = self.current_page
            start_time = time.time()
            
            while page_count <= self.total_pages:
                page_start_time = time.time()
                
                self.logger.info(f"Processing page {page_count}/{self.total_pages}")
                
                # Extract data from current page
                page_data = self.extract_data_from_page()
                
                if page_data:
                    # Add unique records only
                    new_records = 0
                    for record in page_data:
                        if record not in self.all_data:
                            self.all_data.append(record)
                            new_records += 1
                            
                    self.logger.info(f"Added {new_records} new records from page {page_count}")
                    self.logger.info(f"Total records: {len(self.all_data)}")
                else:
                    self.logger.warning(f"No data extracted from page {page_count}")
                
                # Save progress at checkpoints
                if page_count % self.checkpoint_interval == 0:
                    self.save_progress()
                    elapsed_time = time.time() - start_time
                    pages_processed = page_count - (self.current_page - 1)
                    avg_time_per_page = elapsed_time / pages_processed
                    remaining_pages = self.total_pages - page_count
                    estimated_remaining_time = remaining_pages * avg_time_per_page
                    
                    self.logger.info(f"CHECKPOINT: {page_count}/{self.total_pages} pages completed")
                    self.logger.info(f"Average time per page: {avg_time_per_page:.2f} seconds")
                    self.logger.info(f"Estimated time remaining: {estimated_remaining_time/60:.1f} minutes")
                
                # Navigate to next page
                if page_count < self.total_pages:
                    if not self.navigate_to_next_page():
                        self.logger.error(f"Failed to navigate from page {page_count}")
                        break
                        
                page_count += 1
                
                # Small delay between pages
                time.sleep(self.navigation_delay)
                
                # Page timing info
                page_time = time.time() - page_start_time
                self.logger.debug(f"Page {page_count-1} processed in {page_time:.2f} seconds")
            
            # Final save
            self.save_progress()
            
            total_time = time.time() - start_time
            self.logger.info("="*80)
            self.logger.info("EXTRACTION COMPLETED!")
            self.logger.info(f"Total pages processed: {page_count - 1}")
            self.logger.info(f"Total records extracted: {len(self.all_data)}")
            self.logger.info(f"Total time: {total_time/60:.1f} minutes")
            self.logger.info(f"Average time per page: {total_time/(page_count-1):.2f} seconds")
            self.logger.info("="*80)
            
            return len(self.all_data) > 0
            
        except Exception as e:
            self.logger.error(f"Error during full extraction: {e}")
            return False
            
    def save_to_excel(self):
        """Save all extracted data to Excel with formatting"""
        try:
            if not self.all_data:
                self.logger.warning("No data to save")
                return False
                
            # Create DataFrame
            df = pd.DataFrame(self.all_data)
            
            # If first row looks like headers, use it
            if len(df) > 0:
                first_row = df.iloc[0].tolist()
                if any('SL.No' in str(cell).upper() or 'NAME' in str(cell).upper() for cell in first_row):
                    df.columns = first_row
                    df = df.drop(df.index[0]).reset_index(drop=True)
            
            # Save to Excel
            df.to_excel(self.output_file, index=False, engine='openpyxl')
            
            self.logger.info(f"✅ Data saved to: {self.output_file}")
            self.logger.info(f"📊 Final statistics:")
            self.logger.info(f"   Rows: {len(df)}")
            self.logger.info(f"   Columns: {len(df.columns)}")
            
            # Display column names
            if len(df.columns) > 0:
                self.logger.info(f"   Columns: {list(df.columns)}")
            
            # Clean up temporary files
            self.cleanup_temp_files()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving to Excel: {e}")
            return False
            
    def cleanup_temp_files(self):
        """Clean up temporary checkpoint files"""
        try:
            if os.path.exists(self.checkpoint_file):
                os.remove(self.checkpoint_file)
                
            # Remove temp data files
            for file in os.listdir('.'):
                if file.startswith('temp_pib_data_') and file.endswith('.xlsx'):
                    os.remove(file)
                    
            self.logger.info("Temporary files cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up temp files: {e}")
            
    def cleanup(self):
        """Close WebDriver and cleanup"""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
            
    def run(self):
        """Main execution method for full extraction"""
        try:
            print("="*80)
            print("PIB Accredited Media Persons - FULL DATA EXTRACTION v2.0")
            print("="*80)
            print("🎯 Target: ALL 191 pages from PIB India")
            print("🌐 URL: https://accreditation.pib.gov.in/acridexsrch.aspx")
            print(f"📁 Output: {self.output_file}")
            print("🤖 Method: Selenium WebDriver (Optimized)")
            print(f"🔄 Resume from page: {self.current_page}")
            print("-"*80)
            
            # Setup WebDriver
            self.setup_driver()
            
            # Extract all data
            if self.extract_all_data():
                # Save final results
                if self.save_to_excel():
                    print("\n" + "="*80)
                    print("🎉 FULL EXTRACTION COMPLETED SUCCESSFULLY!")
                    print(f"📊 Total records extracted: {len(self.all_data)}")
                    print(f"💾 Data saved to: {self.output_file}")
                    print("📋 Check log file for detailed extraction info")
                    print("="*80)
                    return True
                else:
                    print("❌ ERROR: Failed to save final data")
                    return False
            else:
                print("❌ ERROR: Failed to extract data")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in main execution: {e}")
            print(f"❌ ERROR: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main function"""
    # For production, use headless mode and start from page 1
    extractor = PIBFullExtractor(headless=True, resume_from_page=1)
    return extractor.run()

if __name__ == "__main__":
    main()