from selenium.webdriver.common.by import By
from utils import initialize_driver, save_results_to_excel


# Constants
TEST_URL = "https://www.alojamiento.io/"
SHEET_NAME = "HTML_Tag_Sequence_Test"
# TEST_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
#REPORT_FILE_NAME = "html_tag_sequence_test_report.xlsx"  # Excel file name


# Function to check HTML heading tag sequence [H1-H6]
def check_html_tag_sequence(driver):
    results = []
    try:
        observed_sequence = []
        missing_tags = []
        for i in range(1, 7):
            headings = driver.find_elements(By.TAG_NAME, f"h{i}")
            if headings:
                observed_sequence.append(f"H{i}")
            else:
                missing_tags.append(f"H{i}")

        expected_sequence = [f"H{i}" for i in range(1, 7)]
        if observed_sequence != sorted(observed_sequence, key=lambda x: int(x[1])):
            result = "Fail"
            comment = f"Invalid sequence: {observed_sequence}."
        else:
            comment = "Valid sequence."

        if missing_tags:
            comment += f" Missing tags: {', '.join(missing_tags)}."
            result = "Fail"

        # Log results
        print(f"Observed sequence: {observed_sequence}")
        print(f"Missing tags: {missing_tags}")
        print(f"Comment: {comment}")
    except Exception as e:
        result = "Fail"
        comment = f"Error occurred: {e}"
        print(comment)

    results.append({
        "page_url": driver.current_url,
        "testcase": "HTML Tag Sequence [H1-H6]",
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
        html_tag_results = check_html_tag_sequence(driver)
        save_results_to_excel(html_tag_results, SHEET_NAME)

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()