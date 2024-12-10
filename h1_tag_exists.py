from selenium.webdriver.common.by import By
from utils import initialize_driver, save_results_to_excel


# TEST_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
TEST_URL = "https://www.alojamiento.io/"
SHEET_NAME = "H1_Tag_Test"
#REPORT_FILE_NAME = "h1_tag_test_report.xlsx"


# Function to check H1 tag existence
def check_h1_tag(driver):
    results = []
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        result = "Pass"
        comment = f"H1 tag found: '{h1_tag.text}'"
        # print(comment)
    except Exception as e:
        result = "Fail"
        comment = "H1 tag is missing"
        # print(comment)
    results.append({
        "page_url": driver.current_url,
        "testcase": "H1 Tag Existence",
        "result": result,
        "comments": comment
    })
    return results


# Main Execution
def main():
    driver = initialize_driver()
    try:
        driver.get(TEST_URL)
        print(f"Opened {TEST_URL} successfully!")

        h1_results = check_h1_tag(driver)

        save_results_to_excel(h1_results, SHEET_NAME)

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()