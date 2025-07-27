# Judicial Officers Data Extraction Tool (Version 1)

## Overview
This is the first version of a web scraper designed to extract judicial officers' information from the Madhya Pradesh High Court website (https://mphc.gov.in/judicial-officers). This script uses Selenium WebDriver to automate browser interactions and extract detailed information about judicial officers from various districts.

## Features
- **Automated Web Scraping**: Uses Selenium WebDriver with Chrome in headless mode
- **District-wise Data Extraction**: Iterates through all districts in Madhya Pradesh
- **Detailed Officer Information**: Extracts comprehensive details including:
  - S.No
  - Name
  - Designation
  - Date of Present Posting
  - Father/Mother/Husband Name
  - Join in Judicial date
  - Current District
  - Current Taluka
  - E-mail ID
  - District (where they're listed)

## Technical Implementation
- **Browser Automation**: Chrome WebDriver with headless configuration
- **Anti-Detection**: Includes anti-automation detection measures
- **Retry Mechanism**: Implements click retry functionality with scrolling
- **Modal Handling**: Extracts detailed information from popup modals
- **Data Export**: Saves data to Excel format (`judicial_officers_madhya_pradesh.xlsx`)

## Key Functions
1. **`extract_judicial_officers()`**: Main extraction function that coordinates the entire process
2. **`get_officer_details(driver, officer_id)`**: Extracts personal details from officer modal popup
3. **`click_with_retry(driver, element, max_retries=3)`**: Implements robust clicking with retry logic

## Limitations
- **Limited District Processing**: Currently limited to first 5 districts (`if idx > 4: break`)
- **Basic Error Handling**: Limited error recovery mechanisms
- **No Resume Functionality**: Cannot resume from interruptions
- **Fixed Output**: Always saves to the same filename

## Dependencies
- selenium
- pandas
- openpyxl
- webdriver-manager

## Usage
```python
python extraction.py
```

## Output
The script generates an Excel file named `judicial_officers_madhya_pradesh.xlsx` containing all extracted officer data.

## Notes
- This is the initial version with basic functionality
- Includes random delays to avoid being detected as a bot
- Uses headless browser for efficiency
- Processes districts sequentially with built-in delays
