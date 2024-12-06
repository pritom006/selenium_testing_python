from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# Path to ChromeDriver (use manually downloaded or automated with WebDriverManager)
chromedriver_path = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
service = Service(chromedriver_path)

# Initialize WebDriver and set implicit wait
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

# Test URL
#test_url = "https://www.alojamiento.io/"
test_url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"

# Results list
results = []

try:
    # Open the test site
    driver.get(test_url)
    print(f"Opened {test_url} successfully!")

    # Test 1: Check if H1 tag exists
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        h1_status = "Pass"
        print(f"H1 tag found: {h1_tag.text}")
    except NoSuchElementException:
        h1_status = "Fail"
        print("H1 tag is missing!")

    # Test 2: Validate HTML heading sequence (H1 to H6)
    try:
        headings = [driver.find_elements(By.TAG_NAME, f"h{i}") for i in range(1, 7)]
        heading_sequence = [f"H{i}" for i, heading in enumerate(headings, start=1) if len(heading) > 0]
        if heading_sequence == [f"H{i}" for i in range(1, 7)]:
            heading_status = "Pass"
            print("HTML heading sequence is valid:", heading_sequence)
        else:
            heading_status = "Fail"
            print("HTML heading sequence is invalid or missing elements.")
    except Exception as e:
        heading_status = "Fail"
        print(f"Error validating HTML heading sequence: {e}")

    # Test 3: Validate image alt attributes
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alts = [img for img in images if not img.get_attribute("alt")]
        if len(missing_alts) == 0:
            image_alt_status = "Pass"
            print("All images have valid alt attributes.")
        else:
            image_alt_status = "Fail"
            print(f"{len(missing_alts)} images are missing alt attributes.")
    except Exception as e:
        image_alt_status = "Fail"
        print(f"Error validating image alt attributes: {e}")

    # Test 4: Check URLs for 404 status
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        broken_links = []
        for link in links:
            url = link.get_attribute("href")
            if url:
                response = requests.head(url)
                if response.status_code == 404:
                    broken_links.append(url)
        if len(broken_links) == 0:
            url_status = "Pass"
            print("No broken links found.")
        else:
            url_status = "Fail"
            print(f"Broken links found: {broken_links}")
    except Exception as e:
        url_status = "Fail"
        print(f"Error checking URLs: {e}")

    # Test 5: Perform currency filter test
    try:
        currency_filter = driver.find_element(By.ID, "currency-selector")  # Adjust ID as needed
        currency_filter.click()
        currency_option = driver.find_element(By.XPATH, "//option[@value='USD']")  # Adjust value as needed
        currency_option.click()
        # Verify currency change in property tiles
        property_tiles = driver.find_elements(By.CLASS_NAME, "property-tile")  # Adjust class name as needed
        currency_symbols = [tile.text for tile in property_tiles if "$" in tile.text]
        if len(currency_symbols) > 0:
            currency_status = "Pass"
            print("Currency filter applied successfully.")
        else:
            currency_status = "Fail"
            print("Currency filter did not apply successfully.")
    except Exception as e:
        currency_status = "Fail"
        print(f"Error testing currency filter: {e}")

    # Test 6: Scrape script data and record to Excel
    try:
        script_data = driver.find_elements(By.TAG_NAME, "script")
        scraped_data = {
            "SiteURL": test_url,
            "CampaignID": "N/A",  # Replace with actual extraction logic if needed
            "SiteName": "Alojamiento",
            "Browser": "Chrome",
            "CountryCode": "N/A",  # Replace with actual extraction logic if needed
            "IP": "N/A",  # Replace with actual extraction logic if needed
        }
        results.append(scraped_data)
        print("Script data scraped successfully.")
    except Exception as e:
        print(f"Error scraping script data: {e}")

    # Add all results to a dictionary
    results.append({
        "Test": "H1 Tag Existence",
        "Status": h1_status
    })
    results.append({
        "Test": "HTML Heading Sequence",
        "Status": heading_status
    })
    results.append({
        "Test": "Image Alt Attributes",
        "Status": image_alt_status
    })
    results.append({
        "Test": "Broken URLs",
        "Status": url_status
    })
    results.append({
        "Test": "Currency Filter",
        "Status": currency_status
    })

finally:
    # Save results to Excel
    try:
        df = pd.DataFrame(results)
        df.to_excel("test_results.xlsx", index=False)
        print("Test results saved to 'test_results.xlsx'")
    except Exception as e:
        print(f"Error saving results to Excel: {e}")
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")
