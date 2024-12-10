from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils import initialize_driver, save_results_to_excel
import requests


# Constants
# TEST_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
TEST_URL = "https://www.alojamiento.io/"
SHEET_NAME = "URL_Status_Test"
#REPORT_FILE_NAME = "url_status_report.xlsx"


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
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(links)} links on the page.")

        for link in links:
            url = link.get_attribute("href")
            if url:  # Only process valid URLs
                try:
                    response = requests.head(
                        url, timeout=5)  # Make a HEAD request
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


# Main Execution
def main():
    driver = initialize_driver()
    try:
        driver.get(TEST_URL)
        print(f"Opened {TEST_URL} successfully!")
        url_status_results = check_url_status(driver)
        save_results_to_excel(url_status_results, SHEET_NAME)

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()