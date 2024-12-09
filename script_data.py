from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import os

# Path to ChromeDriver
CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"

# URL of the page to scrape
TEST_URL = "https://www.alojamiento.io/"

# Output file name
OUTPUT_FILE = "script_data_alojamiento.xlsx"

def initialize_driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver

def get_script_data(driver):
    try:
        # Open the target URL
        driver.get(TEST_URL)
        driver.implicitly_wait(5)  # Allow the page to load fully

        # Execute JavaScript to retrieve window.ScriptData
        script_data = driver.execute_script("return window.ScriptData")
        return script_data
    except Exception as e:
        print(f"Error retrieving ScriptData: {e}")
        return None

def process_script_data(script_data):
    try:
        if not script_data:
            return []

        # Extract the required fields from the ScriptData dictionary
        config = script_data.get("config", {})
        user_info = script_data.get("userInfo", {})
        pageData = script_data.get("pageData", {})

        extracted_data = {
            "SiteURL": config.get("SiteUrl", "N/A"),
            "CampaignID": pageData.get("CampaignId", "N/A"),  # Default to "N/A" if not present
            "SiteName": config.get("SiteName", "N/A"),
            "Browser": user_info.get("Platform", "N/A"),
            "CountryCode": user_info.get("CountryCode", "N/A"),
            "IP": user_info.get("IP", "N/A"),
        }

        return [extracted_data]

    except Exception as e:
        print(f"Error processing ScriptData: {e}")
        return []

def save_to_excel(data, file_name):
    """Save extracted data to an Excel file."""
    try:
        # Remove existing file if it exists
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Existing file '{file_name}' removed.")

        # Save to Excel
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
        print(f"Data saved to '{file_name}'")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

if __name__ == "__main__":
    # Initialize the driver
    driver = initialize_driver()
    try:
        # Retrieve ScriptData
        script_data = get_script_data(driver)

        # Process ScriptData and extract relevant fields
        extracted_data = process_script_data(script_data)

        # Save the extracted data to an Excel file
        if extracted_data:
            save_to_excel(extracted_data, OUTPUT_FILE)
        else:
            print("No data extracted.")
    finally:
        driver.quit()
        print("Browser closed.")
