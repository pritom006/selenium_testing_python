from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os

# Constants
CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
#TEST_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
TEST_URL = "https://www.alojamiento.io/"
REPORT_FILE_NAME = "h1_tag_test_report.xlsx"  # Excel file name

# Initialize WebDriver
def initialize_driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    return driver

# Function to check H1 tag existence
def check_h1_tag(driver):
    results = []
    try:
        # Try to find the H1 tag
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        result = "Pass"
        comment = f"H1 tag found: '{h1_tag.text}'"
        print(comment)
    except Exception as e:
        result = "Fail"
        comment = "H1 tag is missing"
        print(comment)
    # Append results
    results.append({
        "page_url": driver.current_url,
        "testcase": "H1 Tag Existence",
        "result": result,
        "comments": comment
    })
    return results

# Save results to Excel
def save_results_to_excel(results, file_name):
    try:
        # Remove existing file if it exists
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Existing file '{file_name}' removed.")

        # Save to Excel
        df = pd.DataFrame(results)
        df.to_excel(file_name, index=False)
        print(f"Report saved to '{file_name}'")
    except Exception as e:
        print(f"Error saving report: {e}")

# Main Execution
if __name__ == "__main__":
    driver = initialize_driver()
    try:
        # Open the test URL
        driver.get(TEST_URL)
        print(f"Opened {TEST_URL} successfully!")

        # Perform H1 tag existence test
        h1_results = check_h1_tag(driver)

        # Save the results to a separate Excel file
        save_results_to_excel(h1_results, REPORT_FILE_NAME)

    finally:
        driver.quit()
        print("Browser closed.")
