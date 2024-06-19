import json
import os
import time
import shutil
import glob
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

target_url = "https://www.jaad.org/issue/S0190-9622(18)X0014-0"
download_dir = os.path.expanduser('~/Downloads')
target_dir = "/home/deck/jguo6/scripts/python/JAAD_CME"

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

print("Log in manually and pass any bot verification as required.")
input("Press Enter to proceed to downloads")

#Navigate to first url

driver.get("https://www.jaad.org/issue/S0190-9622(18)X0014-0")
print("Attempting to get first page")

#After navigating to desired page, give time for page to load
time.sleep(5)

#Parse the page content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all PDF links on the page
base_url = "https://www.jaad.org"
pdf_links = [a['href'] for a in soup.find_all('a', class_='pdfLink')]

# Find all links on the page
all_links = soup.find_all('a', href=True)

pdf_links_and_titles = []

#Iterate through all links to find PDF links and their titles
for i in range(len(all_links)):
    if 'pdfLink' in all_links[i].get('class', []):
        pdf_url = all_links[i]['href']
        # Go back 2 links to get the title
        if i >= 2:
            title_link = all_links[i-2]
            pdf_title = title_link.get_text(strip=True)
            pdf_links_and_titles.append((pdf_url, pdf_title))

# Print and download the PDF links and titles
if pdf_links_and_titles:
    for pdf_url, pdf_title in pdf_links_and_titles:
        print(f"PDF URL: {pdf_url}, Title: {pdf_title}")

    #Download the first 6 PDF links
    for i in range(min(6, len(pdf_links_and_titles))):
        pdf_path, pdf_title = pdf_links_and_titles[i]

        # Construct the full URL
        pdf_url = "https://www.jaad.org" + pdf_path

        print(f"Opening and downloading PDF {i + 1}: {pdf_title}")

        print("The corrected URL is: {}".format(pdf_url))

        #Navigate to the PDF link to trigger the download
        print("Attempting to open PDF")
        driver.get(pdf_url)

        # Wait for PDF to open
        time.sleep(5)

        # Trigger print dialog using Ctrl+P
        print("Printing to save to pdf...")
        pyautogui.hotkey('ctrl', 'p')
        time.sleep(3)
        pyautogui.hotkey('enter')

        # Change how we name the file depending on what i is
        # enter pyautogui to change name to beginning or end as needed
        time.sleep(1)
        pyautogui.hotkey('enter')

        # Find the newest downloaded file in the download directory
        list_of_files = glob.glob(os.path.join(download_dir, '*.pdf'))
        latest_file = max(list_of_files, key=os.path.getctime)

        #Define new file path
        new_file_name = f'pdf_{i + 1}.pdf'
        new_file_path = os.path.join(target_dir, new_file_name)

        #Move and rename file
        shutil.move(latest_file, new_file_path)

        print("Downloaded first PDF as pdf_test.pdf from {}".format(pdf_url))

else:
    print("No PDF links found on the page.")

# Keep the browser open for manual inspection
input("Press Enter to close the browser...")

# Close the browser
driver.quit()

