import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = "/home/w3e17/vacation_rental_testing/chromedriver-linux64/chromedriver"
# REPORT_FILE_PATH = "reports/test_results.xlsx"
REPORT_FILE_PATH = os.path.join("reports", "test_report.xlsx")

def initialize_driver():
    """Initialize and configure Chrome WebDriver."""
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver



def save_results_to_excel(results, sheet_name):
    """
    Save test results to an Excel file under a specific sheet.
    If the file exists, append the new sheet; otherwise, create a new file.
    """
    try:
        # Ensure the "reports" folder exists
        os.makedirs("reports", exist_ok=True)

        if os.path.exists(REPORT_FILE_PATH):
            # File exists, append to it
            with pd.ExcelWriter(REPORT_FILE_PATH, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                df = pd.DataFrame(results)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # File does not exist, create a new one
            with pd.ExcelWriter(REPORT_FILE_PATH, mode="w", engine="openpyxl") as writer:
                df = pd.DataFrame(results)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Results saved in sheet '{sheet_name}' of '{REPORT_FILE_PATH}'")
    except Exception as e:
        print(f"Error saving report: {e}")