"""
Judicial Officers Data Extraction Tool - Version 4.0 (Bug Fix Release)
=======================================================================
Features: Resume functionality, state persistence, multiple execution modes, data management
Bug Fixes: Fixed duplicate records issue when resuming from previous runs
Author: Rahul Dhangar
Last Updated: July 2025
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
import random
import os
import signal

# Version Information
VERSION = "4.0"
VERSION_NAME = "Bug Fix Release - Duplicate Prevention"

ignored_exceptions = (StaleElementReferenceException,)
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

def get_officer_details(driver, officer_id):
    """Extract personal details using improved parsing"""
    details = {}
    
    try:
        wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)
        officer_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[onclick*=\"jinfo('{officer_id}')\"]"))
        )
        
        if not click_with_retry(driver, officer_link):
            print(f"  Failed to click officer ID {officer_id} after retries")
            return details
        
        time.sleep(random.uniform(0.5, 1))
        
        wait.until(EC.presence_of_element_located((By.ID, "jinfo")))
        details_div = driver.find_element(By.ID, "jinfo")
        details_text = details_div.text
        
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, "#facebox .close")
            click_with_retry(driver, close_btn)
            time.sleep(0.3)
        except:
            pass
        
        if details_text:
            lines = [line.strip() for line in details_text.split('\n') if line.strip()]
            
            for line in lines:
                if "Designation" in line:
                    details["Designation"] = line.split("Designation")[-1].strip()
                elif "Present Posting" in line:
                    details["Date of Present Posting"] = line.split("Date of Present Posting")[-1].strip()
                elif "Father" in line or "Mother" in line or "Husband" in line:
                    details["Father/Mother/Husband Name"] = line.split("Father/Mother/Husband Name")[-1].strip()
                elif "Join in Judicial" in line:
                    details["Join in Judicial"] = line.split("Join in Judicial")[-1].strip()
                elif "Current District" in line:
                    details["Current District"] = line.split("Current District")[-1].strip()
                elif "Current Taluka" in line:
                    details["Current Taluka"] = line.split("Current Taluka")[-1].strip()
                elif "E-mail" in line:
                    details["E-mail ID"] = line.split("E-mail ID")[-1].strip()
        
    except Exception as e:
        print(f"  Error getting details for officer ID {officer_id}: {str(e)}")
    
    return details

def load_existing_data(filename):
    """Load existing data from Excel file"""
    if os.path.exists(filename):
        return pd.read_excel(filename).to_dict('records')
    return []

def remove_duplicates_from_data(data):
    """Remove duplicate records based on Name and District combination
    
    BUG FIX v4.0: Added to prevent duplicate records during data loading
    """
    seen = set()
    unique_data = []
    duplicates_found = 0
    
    for record in data:
        key = (record.get('Name', ''), record.get('District', ''))
        if key not in seen:
            seen.add(key)
            unique_data.append(record)
        else:
            duplicates_found += 1
    
    if duplicates_found > 0:
        print(f"🧹 Removed {duplicates_found} duplicate records during data loading")
    
    return unique_data

def save_data(all_officers, filename, overwrite=False):
    """Save data to Excel file with option to overwrite or append"""
    if overwrite or not os.path.exists(filename):
        df = pd.DataFrame(all_officers)
        df.to_excel(filename, index=False)
    else:
        existing_data = load_existing_data(filename)
        combined_data = existing_data + all_officers
        df = pd.DataFrame(combined_data)
        df.to_excel(filename, index=False)

def get_user_choice():
    """Get user choice for resume/update options"""
    print("\n" + "=" * 70)
    print(f"Judicial Officers Extraction Tool v{VERSION} - {VERSION_NAME}")
    print("=" * 70)
    print("🔍 Existing data found!")
    print("🐛 This version includes fixes for duplicate record prevention")
    print("\nExecution Options:")
    print("1. 🔄 Start from beginning (overwrite all data)")
    print("2. 📝 Start from beginning (update only N/A values)")
    print("3. ▶️  Continue from last processed district (FIXED: No more duplicates)")
    print("-" * 70)
    choice = input("Enter your choice (1-3): ").strip()
    
    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please enter 1, 2, or 3.")
        choice = input("Enter your choice (1-3): ").strip()
    
    return int(choice)

def extract_judicial_officers():
    print("=" * 70)
    print(f"Judicial Officers Extraction Tool v{VERSION} - {VERSION_NAME}")
    print("=" * 70)
    print("🚀 Starting advanced data extraction from Madhya Pradesh High Court...")
    print("📁 Output file: Judicial_Officers_MP_v4.xlsx")
    print("💾 State tracking: last_processed_district.txt")
    print("🐛 Bug Fix: Duplicate prevention in resume functionality")
    print("-" * 70)
    
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
    output_file = "Judicial_Officers_MP_v4.xlsx"
    state_file = "last_processed_district.txt"
    
    # Initialize choice variable
    choice = None
    
    # Check if we need to continue from previous run
    start_index = 0
    if os.path.exists(output_file):
        choice = get_user_choice()
        
        if choice == 1:  # Overwrite all
            if os.path.exists(state_file):
                os.remove(state_file)
            all_officers = []
        elif choice == 2:  # Update only N/A values
            all_officers = remove_duplicates_from_data(load_existing_data(output_file))
        elif choice == 3:  # Continue from last district
            # BUG FIX v4.0: Load existing data first to prevent duplicates
            all_officers = remove_duplicates_from_data(load_existing_data(output_file))
            try:
                with open(state_file, 'r') as f:
                    start_index = int(f.read().strip())
                print(f"\nResuming from district index: {start_index + 1}")
                print(f"📊 Loaded {len(all_officers)} existing records")
                start_index += 1
            except:
                print("Could not read state file. Starting from beginning.")
                start_index = 0
    else:
        all_officers = []
        print("\n🆕 Starting fresh extraction...")
        print("-" * 70)
    
    try:
        driver.get("https://mphc.gov.in/judicial-officers")
        
        district_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "menu_dist1"))
        )
        districts = Select(district_dropdown)
        district_names = [option.text for option in districts.options]
        
        for idx in range(start_index, len(district_names)):
            try:
                # Refresh dropdown to avoid stale elements
                district_dropdown = wait.until(
                    EC.presence_of_element_located((By.ID, "menu_dist1"))
                )
                districts = Select(district_dropdown)
                
                district_name = district_names[idx]
                print(f"\nProcessing district: {district_name} ({idx+1}/{len(district_names)})")
                
                districts.select_by_visible_text(district_name)
                time.sleep(random.uniform(3, 5))
                
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table[border='0']")))
                officer_rows = driver.find_elements(By.CSS_SELECTOR, "table[border='0'] tr")
                
                district_officers = []
                for row in officer_rows:
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) < 2:
                            continue
                        
                        officer_link = cells[1].find_element(By.TAG_NAME, "a")
                        officer_name = officer_link.text
                        onclick_text = officer_link.get_attribute("onclick")
                        officer_id = re.search(r"jinfo\('(\d+)'\)", onclick_text).group(1)
                        
                        designation = cells[2].text if len(cells) > 2 else "N/A"
                        court = cells[3].text if len(cells) > 3 else "N/A"
                        
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
                        
                        district_officers.append(officer_data)
                        print(f"  Extracted: {officer_name}")
                        
                    except Exception as e:
                        print(f"  Error processing officer row: {str(e)}")
                        continue
                
                # Update all_officers based on user choice
                if choice == 2:  # Update only N/A values
                    for new_officer in district_officers:
                        key = (new_officer['Name'], new_officer['District'])
                        found = False
                        for existing_officer in all_officers:
                            if (existing_officer['Name'], existing_officer['District']) == key:
                                # Update only N/A values
                                for k, v in new_officer.items():
                                    if existing_officer.get(k) == "N/A":
                                        existing_officer[k] = v
                                found = True
                                break
                        if not found:
                            all_officers.append(new_officer)
                elif choice == 3:  # Resume - avoid duplicates by checking if district already processed
                    # BUG FIX v4.0: Remove existing data for this district to prevent duplicates
                    original_count = len(all_officers)
                    all_officers = [officer for officer in all_officers if officer.get('District') != district_name]
                    removed_count = original_count - len(all_officers)
                    if removed_count > 0:
                        print(f"  🔄 Removed {removed_count} existing records for {district_name} to avoid duplicates")
                    # Add new data for this district
                    all_officers.extend(district_officers)
                    print(f"  ✅ Added {len(district_officers)} new records for {district_name}")
                else:  # choice == 1 - overwrite all
                    all_officers.extend(district_officers)
                
                # BUG FIX v4.0: Always overwrite during save to prevent duplicate accumulation
                save_data(all_officers, output_file, overwrite=True)
                with open(state_file, 'w') as f:
                    f.write(str(idx))
                
                time.sleep(random.uniform(4, 6))
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing district {idx} ({district_name}): {str(e)}")
                continue
        
        # BUG FIX v4.0: Final save with overwrite to ensure data consistency
        save_data(all_officers, output_file, overwrite=True)
        print("\n" + "=" * 70)
        print(f"🎉 SUCCESS: Extraction completed using v{VERSION}")
        print(f"📊 Total officers extracted: {len(all_officers)}")
        print(f"💾 Data saved to: {output_file}")
        print(f"🔧 Version features: {VERSION_NAME}")
        print("🐛 Bug fixes: Duplicate prevention in resume functionality")
        print("=" * 70)
        
    finally:
        # Only delete state file if script completed successfully
        # We'll handle cleanup in a separate function that's called on successful completion
        driver.quit()
        print("WebDriver closed successfully")

def cleanup_on_success():
    """Clean up state file only on successful completion"""
    state_file = "last_processed_district.txt"
    if os.path.exists(state_file):
        os.remove(state_file)
        print("State file cleaned up successfully")

if __name__ == "__main__":
    try:
        extract_judicial_officers()
        cleanup_on_success()  # Only clean up if script completes successfully
    except KeyboardInterrupt:
        print("\nScript interrupted by user. State file preserved for resuming.")
    except Exception as e:
        print(f"\nScript terminated with error: {str(e)}. State file preserved for resuming.")