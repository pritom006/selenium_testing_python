from selenium.webdriver.common.by import By
from utils import initialize_driver, save_results_to_excel
import requests


# Constants
TEST_URL = "https://www.alojamiento.io/"
SHEET_NAME = "Image_Alt_Attributes_Test"
#REPORT_FILE_NAME = "image_alt_attribute_test_report.xlsx"  # Excel file name


# Function to check Image Alt Attribute
def check_image_alt_attribute(driver):
    results = []
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(images)} images on the page.")

        missing_alts = []
        for img in images:
            alt = img.get_attribute("alt")
            img_url = img.get_attribute("src")
            if not alt:
                # Add the image URL to the missing list
                missing_alts.append(img_url)

        # Determine the result
        if missing_alts:
            result = "Fail"
            comment = f"Missing alt attributes for images: {
                ', '.join(missing_alts)}"
        else:
            result = "Pass"
            comment = "All images have alt attributes."

        # Log the results
        print(f"Missing alt attributes for images: {
              missing_alts}" if missing_alts else "All images have alt attributes.")
    except Exception as e:
        result = "Fail"
        comment = f"Error occurred: {e}"
        print(comment)

    results.append({
        "page_url": driver.current_url,
        "testcase": "Image Alt Attribute Test",
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
        image_alt_results = check_image_alt_attribute(driver)
        save_results_to_excel(image_alt_results, SHEET_NAME)

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()