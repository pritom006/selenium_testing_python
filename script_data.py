from selenium.webdriver.common.by import By
from utils import initialize_driver, save_results_to_excel


TEST_URL = "https://www.alojamiento.io/"
SHEET_NAME = "Script_Data_Test"
#OUTPUT_FILE = "script_data_alojamiento.xlsx"


def get_script_data(driver):
    try:
        driver.get(TEST_URL)
        driver.implicitly_wait(5)  # Allow the page to load fully
        script_data = driver.execute_script("return window.ScriptData")
        return script_data
    except Exception as e:
        print(f"Error retrieving ScriptData: {e}")
        return None


def process_script_data(script_data):
    try:
        if not script_data:
            return []

        config = script_data.get("config", {})
        user_info = script_data.get("userInfo", {})
        pageData = script_data.get("pageData", {})

        extracted_data = {
            "SiteURL": config.get("SiteUrl", "N/A"),
            "CampaignID": pageData.get("CampaignId", "N/A"),
            "SiteName": config.get("SiteName", "N/A"),
            "Browser": user_info.get("Browser", "N/A"),
            "CountryCode": user_info.get("CountryCode", "N/A"),
            "IP": user_info.get("IP", "N/A"),
        }

        return [extracted_data]

    except Exception as e:
        print(f"Error processing ScriptData: {e}")
        return []

def main():
    driver = initialize_driver()
    try:
        script_data = get_script_data(driver)
        extracted_data = process_script_data(script_data)

        if extracted_data:
            save_results_to_excel(extracted_data, SHEET_NAME)
        else:
            print("No data extracted.")
    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()