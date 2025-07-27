"""
Judicial Officers Data Extraction Tool - Version 1.0
====================================================
Features: Basic web scraping functionality, limited to 5 districts
Author: Rahul Dhangar
Last Updated: July 2025
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
import random

# Version Information
VERSION = "1.0"
VERSION_NAME = "Basic Functionality"

ignored_exceptions=(StaleElementReferenceException,)

def click_with_retry(driver, element, max_retries=3):
    """Retry clicking with scrolling"""
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"  Click attempt {attempt + 1} failed: {str(e)}")
            time.sleep(1)
    return False

def extract_judicial_officers():
    print("=" * 60)
    print(f"Judicial Officers Extraction Tool v{VERSION} - {VERSION_NAME}")
    print("=" * 60)
    print("Starting basic data extraction from Madhya Pradesh High Court...")
    print(f"Output file: judicial_officers_madhya_pradesh.xlsx")
    print("⚠️  Note: Limited to first 5 districts in this version")
    print("-" * 60)
    
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    
    all_officers = []
    
    try:
        driver.get("https://mphc.gov.in/judicial-officers")
        
        # Get all district options
        district_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "menu_dist1"))
        )
        
        districts = Select(district_dropdown)
        district_options = districts.options
        
        for idx in range(0, len(district_options)):
            if idx > 4: 
                break
            try:
                district_name = district_options[idx].text
                print(f"\nProcessing district: {district_name} ({idx+1}/{len(district_options)})")
                # Deselect all options first (in case of multi-select)
                #for option in district_options:
                #    if option.is_selected():
                #        districts.deselect_by_visible_text(option.text)
                # Select the current district
                districts.select_by_visible_text(district_name)
                # Wait for the page to update
                time.sleep(random.uniform(3, 5))
                # Wait for officer list to load
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table[border='0']")))
                # Get all officer rows
                officer_rows = driver.find_elements(By.CSS_SELECTOR, "table[border='0'] tr")
                
                for row in officer_rows:
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) < 2:
                            continue
                        
                        # Extract officer details
                        officer_link = cells[1].find_element(By.TAG_NAME, "a")
                        officer_name = officer_link.text
                        onclick_text = officer_link.get_attribute("onclick")
                        officer_id = re.search(r"jinfo\('(\d+)'\)", onclick_text).group(1)
                        
                        designation = cells[2].text if len(cells) > 2 else "N/A"
                        court = cells[3].text if len(cells) > 3 else "N/A"
                        
                        # Get personal details
                        personal_details = get_officer_details(driver, officer_id)
                        
                        officer_data = {
                            "S.No": cells[0].text if len(cells) > 0 else "N/A",
                            "Name": officer_name,
                            "Designation": personal_details.get("Designation", "N/A"),
                            "Date of Present Posting": personal_details.get("Date of Present Posting", "N/A"),
                            "Father/Mother/Husband Name": personal_details.get("Father/Mother/Husband Name", "N/A"),
                            "Join in Judicial": personal_details.get("Join in Judicial", "N/A"),
                            "Current District": personal_details.get("Current District", "N/A"),
                            "Current Taluka": personal_details.get("Current Taluka", "N/A"),
                            "E-mail ID": personal_details.get("E-mail ID", "N/A"),
                            "District": district_name
                        }
                        
                        all_officers.append(officer_data)
                        print(f"  Extracted: {officer_name}")
                        
                    except Exception as e:
                        print(f"  Error processing officer row: {str(e)}")
                        continue
                # Add a longer delay after processing each district
                time.sleep(random.uniform(4, 6))
                # Scroll to avoid stale elements
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing district {idx} ({district_name}): {str(e)}")
                # Refresh the dropdown if there's an error
                try:
                    district_dropdown = driver.find_element(By.ID, "menu_dist1")
                    districts = Select(district_dropdown)
                    district_options = districts.options
                except:
                    print("  Could not refresh district dropdown, continuing...")
                    continue
        
        # Get all district options
        district_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "menu_dist1"))
        )
        districts = Select(district_dropdown)
    finally:
        time.sleep(1)
        driver.quit()
    
    # Save to Excel
    if all_officers:
        df = pd.DataFrame(all_officers)
        df.to_excel("judicial_officers_madhya_pradesh.xlsx", index=False)
        print("=" * 60)
        print(f"✓ SUCCESS: Extraction completed using v{VERSION}")
        print(f"✓ Total officers extracted: {len(all_officers)}")
        print(f"✓ Data saved to: judicial_officers_madhya_pradesh.xlsx")
        print("=" * 60)
    else:
        print("❌ ERROR: No data extracted. Check selectors or website structure.")

def get_officer_details(driver, officer_id):
    """Extract personal details using improved parsing"""
    details = {}
    
    try:
        # Find the officer link element
        wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)
        officer_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[onclick*=\"jinfo('{officer_id}')\"]"))
        )
        
        # Use retry mechanism to click
        if not click_with_retry(driver, officer_link):
            print(f"  Failed to click officer ID {officer_id} after retries")
            return details
        
        time.sleep(random.uniform(0.5, 1))
        
        # Wait for modal content
        wait.until(EC.presence_of_element_located((By.ID, "jinfo")))
        
        # Get details text
        details_div = driver.find_element(By.ID, "jinfo")
        details_text = details_div.text
        
        # Close modal
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, "#facebox .close")
            click_with_retry(driver, close_btn)
            time.sleep(0.3)
        except:
            pass
        
        # Parse specific fields
        if details_text:
            lines = [line.strip() for line in details_text.split('\n') if line.strip()]
            
            # Extract specific fields based on patterns
            for line in lines:
                # Designation
                if "Designation" in line:
                    details["Designation"] = line.split("Designation")[-1].strip()
                # Date of Present Posting
                elif "Present Posting" in line:
                    details["Date of Present Posting"] = line.split("Date of Present Posting")[-1].strip()
                # Father/Mother/Husband Name
                elif "Father" in line or "Mother" in line or "Husband" in line:
                    details["Father/Mother/Husband Name"] = line.split("Father/Mother/Husband Name")[-1].strip()
                # Join in Judicial
                elif "Join in Judicial" in line:
                    details["Join in Judicial"] = line.split("Join in Judicial")[-1].strip()
                # Current District
                elif "Current District" in line:
                    details["Current District"] = line.split("Current District")[-1].strip()
                # Current Taluka
                elif "Current Taluka" in line:
                    details["Current Taluka"] = line.split("Current Taluka")[-1].strip()
                # E-mail ID
                elif "E-mail" in line:
                    details["E-mail ID"] = line.split("E-mail ID")[-1].strip()
        
    except Exception as e:
        print(f"  Error getting details for officer ID {officer_id}: {str(e)}")
    
    return details

if __name__ == "__main__":
    extract_judicial_officers()