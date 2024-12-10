from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import initialize_driver, save_results_to_excel
import time


# Constants
TEST_URL = "https://www.alojamiento.io/"
SHEET_NAME = "Currency_Filter_Test"
#REPORT_FILE_NAME = "currency_filter_test_report.xlsx"

# Currencies to test
CURRENCIES = [
    {"symbol": "$ (USD)", "country": "US"},
    {"symbol": "$ (CAD)", "country": "CA"},
    {"symbol": "€ (EUR)", "country": "BE"},
    {"symbol": "£ (GBP)", "country": "IE"},
    {"symbol": "$ (AUD)", "country": "AU"},
    {"symbol": "$ (SGD)", "country": "SG"},
    {"symbol": "د.إ. (AED)", "country": "AE"},
    {"symbol": "৳ (BDT)", "country": "BD"}
]


def check_currency_filter(driver):
    """Perform currency filter tests for all currencies."""
    results = []
    try:
        driver.get(TEST_URL)
        print(f"Opened {TEST_URL} successfully!")

        # Wait for page to load completely
        time.sleep(5)

        # Test each currency
        for currency in CURRENCIES:
            result = test_single_currency(driver, currency)
            results.append(result)

    except Exception as e:
        print(f"Overall test error: {e}")
        results.append({
            "page_url": driver.current_url,
            "testcase": "Currency Filter Test - Overall",
            "result": "Fail",
            "comments": f"Unexpected error: {e}"
        })

    return results


def test_single_currency(driver, currency):
    """Test a single currency selection."""
    try:
        # Scroll to the footer to locate the currency dropdown
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Save the results to a separate Excel file
        # Find and click the currency dropdown using CSS selector
        currency_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".select-wrap"))
        )
        driver.execute_script("arguments[0].click();", currency_dropdown)
        time.sleep(1)

        # Find and click the specific currency from the dropdown
        currency_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,        # Save the results to a separate Excel file
                 f".select-ul li[data-currency-country='{currency['country']}']")
            )
        )
        driver.execute_script("arguments[0].click();", currency_item)
        print(f"Selected currency: {currency['symbol']}")

        # Wait for page content to update
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, "js-currency-sort-footer"), currency['symbol'])
        )
        time.sleep(2)

        # Scroll back to the property section to check for changes
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        # Fetch property tiles and price information
        property_tiles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "property-tiles"))
        )
        price_info = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "js-price-value"))
        )

        # Verify content for the selected currency
        if not property_tiles or not price_info:
            return {
                "page_url": driver.current_url,
                "testcase_url": f"Currency Filter - {currency['symbol']}",
                "result": "Inconclusive",
                "comments": "No property tiles or price info found to verify currency change"
            }

        # Extract text for verification
        tile_texts = [tile.text for tile in property_tiles]
        price_texts = [price.text for price in price_info]

        print(f"Currency: {currency['symbol']}")
        print(f"Property Tiles Text: {tile_texts}")
        print(f"Price Info Text: {price_texts}")

        # Verify if the correct currency symbol is present in the texts
        # Use the first part of the symbol
        expected_symbol = currency['symbol'].split()[0]
        symbol_match_tiles = any(
            expected_symbol in text for text in tile_texts)
        symbol_match_prices = any(
            expected_symbol in text for text in price_texts)

        if symbol_match_tiles and symbol_match_prices:
            result = "Pass"
            comment = f"Currency changed to {currency['symbol']} successfully."
        else:
            result = "Fail"
            comment = f"Currency change to {
                currency['symbol']} not reflected correctly."

        return {
            "page_url": driver.current_url,
            "testcase": f"Currency Filter - {currency['symbol']}",
            "result": result,
            "comments": comment
        }

    except Exception as e:
        return {
            "page_url": driver.current_url,
            "testcase": f"Currency Filter - {currency['symbol']}",
            "result": "Fail",
            "comments": f"Error selecting currency {currency['symbol']}: {e}"
        }


# Main Execution
def main():
    driver = initialize_driver()
    try:
        currency_filter_results = check_currency_filter(driver)
        save_results_to_excel(currency_filter_results, SHEET_NAME)

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()