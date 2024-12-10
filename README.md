# Vacation Rental Home Page Automation Testing

This project automates testing for vacation rental websites using Python, Selenium, and Pandas. The results of each test are stored in organized Excel reports for further analysis.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Available Tests](#available-tests)
- [Reports](#reports)
- [Acknowledgments](#acknowledgments)


---

## Project Overview

The Vacation Rental Website Testing Automation project is designed to validate the functionality of key components of vacation rental websites. It ensures the presence of essential elements like H1 tags, broken links, and image loading. This is useful for maintaining the quality of vacation rental platforms and identifying potential issues.

---

## Features

- Automated testing using Selenium WebDriver.
- Configurable test URLs.
- Modular structure with reusable components.
- Generates reports in Excel format, with each test saved as a separate sheet.
- Stores reports in a structured `reports/` directory.

---

## Project Structure

```bash
VACATION_RENTAL_TESTING/
├── __pycache__/
├── chromedriver-linux64/
├── reports/
│   └── test_report.xlsx
├── venv/
├── .gitignore
├── currency_filtering.py
├── h1_tag_exists.py
├── html_tag_sequence.py
├── image_alt_attribute.py
├── requirements.txt
├── run_all_tests.py
├── script_data.py
├── url_status_test.py
├── utils.py
```

---


## Installation

### Prerequisites

- Python 3.8 or above
- Google Chrome and ChromeDriver
- pip (Python package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/vacation_rental_testing.git
   cd vacation_rental_testing
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up ChromeDriver:**
   ```bash
   Ensure that ChromeDriver is installed and matches your Chrome browser version. Add it to your system's PATH.
   My Case: CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
   ```


## Usage

### Running Individual Tests

1. **Check H1 Tag Existence:**
   ```bash
   python h1_tag_exists.py
   ```

2. **Check HTML Tag Sequence Test:**
   ```bash
   python html_tag_sequence.py
   ```

3. **Check Img alt attribute Test:**
   ```bash
   python image_alt_attribute.py
   ```

4. **URL status code test of URLs:**
   ```bash
   python url_status_test.py
   ```

5. **Currency Filtering test:**
   ```bash
   python currency_filtering.py
   ```

6. **Scrape data from Script Data:**
   ```bash
   python script_data.py
   ```

### Run All Test Case Together   
   **To run all test use:**
   ```bash
   python run_all_tests.py
   ```


## Available Tests

### H1 Tag Test (`h1_tag_exists.py`)
> **:white_check_mark: Validates the presence of H1 tags on a webpage.**

### HTML Tag Sequence Check (`h1_tag_exists.py`)
> **:white_check_mark: [H1-H6] tag available if any of the sequence
broken or missing it should be reported as fail.
If any tag is missing its report that tag is missing and Check valid and Invalid Sequence**

### Image alt attribute Test (`image_alt_attribute.py`)
> **:white_check_mark: Checks if all images have alt attribute on a webpage load successfully.**

### URL status code test of URLs (`url_status_test.py`)
> **:white_check_mark: if any URL status is 404 it should be reported as Fail otherwise Pass**

### Currency Filtering test of Different Region (`currency_filtering.py`)
> **:white_check_mark: it checks the cuurency in footer with card body that the currency should be 
changed according their region currency, if it pass the test then return Pass otherwise Fail.**

### Scrape data from Script data
> **:white_check_mark: from window.ScriptData dictionary collect the SiteURL, CampaignID, SiteName, Browser, CountryCode, IP.**


## Reports
> **:white_check_mark: All test results are saved in an Excel file (`test_report.xlsx`) located in the `reports/` directory. Each test's results are stored in separate sheets for easy navigation.**


## Acknowledgments

This project utilizes the following libraries and tools:

- [Selenium](https://www.selenium.dev/)
- [Pandas](https://pandas.pydata.org/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)
