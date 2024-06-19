import json
import os
import re
import time
import shutil
import glob
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

#Define file paths and directories
url_file_path = "/home/deck/jguo6/scripts/python/JAAD_CME/jaad_urls.txt"
base_download_dir = os.path.expanduser('~/Downloads')
base_target_dir = "/home/deck/jguo6/scripts/python/JAAD_CME/JG_CME_Downloads"

# Create the base target directory if it doesn't exist already
if not os.path.exists(base_target_dir):
    os.makedirs(base_target_dir)

# Function to get month in MM format
def get_month_number(month_name):
    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    return f"{month_names.index(month_name) + 1:02d}"

# Set up the Selenium WebDriver with ChromeDriver bundled with Chrome
print("Setting up Selenium options")
options = webdriver.ChromeOptions()

# Run chrome in debug with this command
#    flatpak run com.google.Chrome --remote-debugging-port=9222 --user-data-dir="/home/deck/jguo6/scripts/python/JAAD_CME/custom_chrome_profile"
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#Connect to existing Chrome instance
print("Attempting to connect to chrome instance")
driver = webdriver.Chrome(options=options)

# Navigate to the login page
#driver.get("https://identity.aad.org/?ReturnUrl=%2Felsevier")
#print("Attempting to navigate to login page")

print("Log in manually and pass any bot verification as required.")
input("Press Enter to proceed to downloads")

# Parse the URL file
print("Attempting to parse file")
with open(url_file_path, 'r') as file:
    lines = file.readlines()

# Function to remove part identifier from title
def remove_part_identifier(title):
    return re.sub(r'\b(part\s*(1|2|I|II)[\.:]?)\b', '', title, flags=re.IGNORECASE).strip()


# Loop through each line in the URL file
for line in lines:
    # Extract the URL, month, and year from the line
    url, date_info = line.strip().split(' for ')
    month, year = date_info.split(' ')
    month_number = get_month_number(month)
    #print(f"URL is {url}, month is {month} and year is {year}")

    # Construct the month-year directory path
    month_year_dir = os.path.join(base_target_dir, year, f"{month_number}_{year} {month)")

    #print(f"month_year_dir directory is {month_year_dir}")

    # Delete the existing month folder and recreate it
    if os.path.exists(month_year_dir):
        shutil.rmtree(month_year_dir)
    os.makedirs(month_year_dir, exist_ok=True)

    # Navigate to the URL
    driver.get(url)
    #print(f"Attempting to get page for {month} {year}")
    print(" ")
    print(" ")
    print(" ")

    #After navigating to desired page, give time for page to load
    time.sleep(2)

    #Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all links on the page
    all_links = soup.find_all('a', href=True)

    # List to store PDF URLs and titles
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
        #for pdf_url, pdf_title in pdf_links_and_titles:
        #    print(f"PDF URL: {pdf_url}, Title: {pdf_title}")

        #Download the first 6 PDF links
        for i in range(min(6, len(pdf_links_and_titles))):
            pdf_path, pdf_title = pdf_links_and_titles[i]
    
            # Construct the full URL
            pdf_url = "https://www.jaad.org" + pdf_path
    
            #print(f"Opening and downloading PDF {i + 1}: {pdf_title}")
    
            #print("The corrected URL is: {}".format(pdf_url))
    
            #Navigate to the PDF link to trigger the download
            #print("Attempting to open PDF")
            driver.get(pdf_url)
            print(" ")
    
            # Wait for PDF to open
            time.sleep(2)
    
            # Trigger print dialog using Ctrl+P
            #print("Printing to save to pdf...")
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(1)
            pyautogui.hotkey('enter')
            time.sleep(1)
            pyautogui.hotkey('enter')
    
            # Find the newest downloaded file in the download directory
            list_of_files = glob.glob(os.path.join(base_download_dir, '*.pdf'))
            latest_file = max(list_of_files, key=os.path.getctime)
    
            #Define new file path
            base_file_name = f"{month} {year} -"

            if i == 0:
                pdf_title = remove_part_identifier(pdf_title)
                new_file_name = f"{base_file_name} {pdf_title} part I.pdf"
            elif i == 3:
                pdf_title = remove_part_identifier(pdf_title)
                new_file_name = f"{base_file_name} {pdf_title} part II.pdf"
            elif i in [1, 2]:
                if pdf_title == "PDF":
                    new_file_name = f"{base_file_name} CME exam answers 1.pdf"
                elif "CME examinations" in pdf_title or "CME" in pdf_title or "examination" in pdf_title:
                    new_file_name = f"{base_file_name} CME examination 1.pdf"
                else:
                    print("!!! WARNING UNKNOWN FILE !!!")
                    new_file_name = f"{base_file_name} UNKNOWN {i}"
            elif i in [4, 5]:
                if pdf_title == "PDF":
                    new_file_name = f"{base_file_name} CME exam answers 2.pdf"
                elif "CME examinations" in pdf_title or "CME" in pdf_title or "examination" in pdf_title:
                    new_file_name = f"{base_file_name} CME examination 2.pdf"
                else:
                    print("!!!WARNING UNKNOWN FILE !!!")
                    new_file_name = f"{base_file_name} UNKNOWN {i}"
            else:
                new_file_name = f"{base_file_name} {pdf_title}.pdf"

            new_file_path = os.path.join(month_year_dir, new_file_name.replace("/", "_"))

            #Move and rename file
            try:
                shutil.move(latest_file, new_file_path)
            except Exception as e:
                print(f"** ERROR Failed to move {latest_file} to {new_file_path}: {e}!!!!")

            print("*************************************************************************** ")
            print(" ")
            print(f"Downloaded PDF {i+1} for {month} {year}")
            print(f"Original file name:   {pdf_title}")
            print(f"New file name:        {new_file_name}")
            print(f"PDF URL:              {pdf_url}")
            print(f"Saved to directory {new_file_path} ")
            print(" ")
            print("*************************************************************************** ")
            print(" ")


else:
    print("No PDF links found on the page.")

# Keep the browser open for manual inspection
input("Press Enter to close the browser...")

# Close the browser
driver.quit()

