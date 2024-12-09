from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import pandas as pd
import os

# Constants
CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
TEST_URL = "https://www.alojamiento.io/"
REPORT_FILE_NAME = "image_alt_attribute_test_report.xlsx"  # Excel file name

# Initialize WebDriver
def initialize_driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    return driver

# Function to check Image Alt Attribute
def check_image_alt_attribute(driver):
    results = []
    try:
        # Find all images on the page
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(images)} images on the page.")

        missing_alts = []  # List to hold images missing the alt attribute
        for img in images:
            alt = img.get_attribute("alt")
            img_url = img.get_attribute("src")
            if not alt:
                missing_alts.append(img_url)  # Add the image URL to the missing list

        # Determine the result
        if missing_alts:
            result = "Fail"
            comment = f"Missing alt attributes for images: {', '.join(missing_alts)}"
        else:
            result = "Pass"
            comment = "All images have alt attributes."

        # Log the results
        print(f"Missing alt attributes for images: {missing_alts}" if missing_alts else "All images have alt attributes.")
    except Exception as e:
        result = "Fail"
        comment = f"Error occurred: {e}"
        print(comment)

    # Append results to the list
    results.append({
        "page_url": driver.current_url,
        "testcase": "Image Alt Attribute Test",
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

        # Perform Image Alt Attribute test
        image_alt_results = check_image_alt_attribute(driver)

        # Save the results to a separate Excel file
        save_results_to_excel(image_alt_results, REPORT_FILE_NAME)

    finally:
        driver.quit()
        print("Browser closed.")
