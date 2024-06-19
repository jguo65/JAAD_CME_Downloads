import json
import os
import time
import shutil
import glob
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Define your credentials
username = "shzhang49@gmail.com"
password = "zqm3qpu6GBH-zdh@qmx"


target_url = "https://www.jaad.org/issue/S0190-9622(18)X0014-0"
download_dir = os.path.expanduser('~/Downloads')
target_dir = "/home/deck/jguo6/scripts/python/JAAD_CME"
new_file_name = 'pdf_test.pdf'

print("Login credentials confirmed")

# Set up the Selenium WebDriver with ChromeDriver bundled with Chrome
print("Setting up Selenium options")
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#Connect to existing Chrome instance
print("Attempting to connect to chrome instance")
driver = webdriver.Chrome(options=options)

# Navigate to the login page
#driver.get("https://identity.aad.org/?ReturnUrl=%2Felsevier")
print("Attempting to navigate to login page")

input("Press Enter to proceed to downloads")

## Give the page some time to load
#time.sleep(5)
#
##hardcode login
#actions = webdriver.ActionChains(driver)
#actions.send_keys(username)
#actions.send_keys(Keys.TAB)
#actions.send_keys(password)
#actions.send_keys(Keys.TAB)
#actions.send_keys(Keys.TAB)
#actions.send_keys(Keys.RETURN)
#actions.perform()
#print("Login fields found, attempting to login")
#
## Give the login process some time to complete
#time.sleep(5)
#
## Verify if login was successful by checking the URL or page content
#if "ReturnUrl" not in driver.current_url:
#    print("Login successful")
#else:
#    print("Login failed")


#Navigate to first url

driver.get("https://www.jaad.org/issue/S0190-9622(18)X0014-0")
print("Attempting to get first page")

#After navigating to desired page, give time for page to load
time.sleep(5)

#Parse the page content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all PDF links on the page
pdf_links = [a['href'] for a in soup.find_all('a', class_='pdfLink')]

# Print the list of PDF links
if pdf_links:
    for link in pdf_links:
        print(link)

    # Download the first PDF link
    first_pdf_url = pdf_links[0]

    # Make sure the URL is absolute
    if not first_pdf_url.startswith('http'):
            print("URL is not absolute!!")
            first_pdf_url = driver.current_url.rsplit('/', 1)[0] + '/' + first_pdf_url

    # Remove the extra "issue/" if present
    first_pdf_url = first_pdf_url.replace('/issue/', '')

    print("The corrected URL is: {}".format(first_pdf_url))

    # Navigate to the PDF link to trigger the download
    print("Attempting to open pdf")
    driver.get(first_pdf_url)

    # Wait for PDF to open
    time.sleep(3)

    # Trigger print dialog using Ctrl+P
    print("Printing to save to pdf...")
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(3)
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.hotkey('enter')
    input("Press enter after successfully printing")

    # Find the newest downloaded file in the download directory
    list_of_files = glob.glob(os.path.join(download_dir, '*.pdf'))
    latest_file = max(list_of_files, key=os.path.getctime)

    #Define new fiel path
    new_file_path = os.path.join(target_dir, new_file_name)

    #Move and rename file
    shutil.move(latest_file, new_file_path)

    print("Downloaded first PDF as pdf_test.pdf from {}".format(first_pdf_url))

else:
    print("No PDF links found on the page.")

# Keep the browser open for manual inspection
input("Press Enter to close the browser...")

# Close the browser
driver.quit()

