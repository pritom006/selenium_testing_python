from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os

# Constants
CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
TEST_URL = "https://www.alojamiento.io/"
#TEST_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
REPORT_FILE_NAME = "html_tag_sequence_test_report.xlsx"  # Excel file name

# Initialize WebDriver
def initialize_driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    return driver

# Function to check HTML heading tag sequence [H1-H6]
def check_html_tag_sequence(driver):
    results = []
    try:
        # Collect all heading tags (H1 to H6) and their order from the page
        observed_sequence = []
        missing_tags = []
        for i in range(1, 7):
            headings = driver.find_elements(By.TAG_NAME, f"h{i}")
            if headings:
                observed_sequence.append(f"H{i}")
            else:
                missing_tags.append(f"H{i}")

        # Determine the result
        expected_sequence = [f"H{i}" for i in range(1, 7)]
        if observed_sequence != sorted(observed_sequence, key=lambda x: int(x[1])):
            result = "Fail"
            comment = f"Invalid sequence: {observed_sequence}."
        else:
            comment = "Valid sequence."

        # Add missing tags to the comment, if any
        if missing_tags:
            comment += f" Missing tags: {', '.join(missing_tags)}."
            result = "Fail"  # Ensure the result is Fail if any tags are missing

        # Log results
        print(f"Observed sequence: {observed_sequence}")
        print(f"Missing tags: {missing_tags}")
        print(f"Comment: {comment}")
    except Exception as e:
        result = "Fail"
        comment = f"Error occurred: {e}"
        print(comment)

    # Append results
    results.append({
        "page_url": driver.current_url,
        "testcase": "HTML Tag Sequence [H1-H6]",
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

        # Perform HTML tag sequence test
        html_tag_results = check_html_tag_sequence(driver)

        # Save the results to a separate Excel file
        save_results_to_excel(html_tag_results, REPORT_FILE_NAME)

    finally:
        driver.quit()
        print("Browser closed.")
