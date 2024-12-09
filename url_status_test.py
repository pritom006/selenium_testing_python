from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import os

# Constants
CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
#TEST_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
TEST_URL = "https://www.alojamiento.io/"
REPORT_FILE_NAME = "url_status_report.xlsx"  # Excel file name

# Initialize WebDriver
def initialize_driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    return driver

# Map status codes to comments with status code in brackets
def get_status_comment(status_code):
    if status_code == 200:
        return f"Successful URL ({status_code})"
    elif status_code == 404:
        return f"Page Not Found ({status_code})"
    elif status_code == 403:
        return f"Forbidden ({status_code})"
    elif status_code == 500:
        return f"Internal Server Error ({status_code})"
    elif status_code == 301 or status_code == 302:
        return f"Redirected ({status_code})"
    else:
        return f"Unknown Status ({status_code})"

# Function to check URL status
def check_url_status(driver):
    results = []  # Store results for Excel report
    try:
        # Find all anchor tags on the page
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(links)} links on the page.")

        for link in links:
            url = link.get_attribute("href")  # Get the href attribute
            if url:  # Only process valid URLs
                try:
                    response = requests.head(url, timeout=5)  # Make a HEAD request
                    status_code = response.status_code
                    result = "Pass" if status_code == 200 else "Fail"
                    comment = get_status_comment(status_code)
                except requests.RequestException as e:
                    status_code = "Error"
                    result = "Fail"
                    comment = f"Error: {e}"
                    print(f"Error checking URL {url}: {e}")
                results.append({
                    "page_url": driver.current_url,
                    "testcase_url": url,
                    "result": result,
                    "comments": comment
                })
    except Exception as e:
        print(f"Error extracting URLs: {e}")
    return results

# Save results to Excel
def save_results_to_excel(results, file_name):
    try:
        # Debug log: Print working directory
        print(f"Current working directory: {os.getcwd()}")

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

        # Perform URL status test
        url_status_results = check_url_status(driver)

        # Save the results to an individual Excel file
        save_results_to_excel(url_status_results, REPORT_FILE_NAME)

    finally:
        driver.quit()
        print("Browser closed.")

