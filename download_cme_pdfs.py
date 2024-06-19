'''
JAAD CME Download script

This script taks in the jaad_urls.txt file genereated from cme_urls.py, goes to each URL
and downloads both part 1 and part 2 CME Journals and their corresponding exams/answer keys.

Per Duaa's requirements:

- All files are prepended by "{month} {year} -"
- The journal articles end in part (I|II).pdf
- The exams are saved as CME examination (1|2).pdf
- The exam answers are saved as CME exam answers (1|2).pdf

The script makes a folder for each year. Each year folder will have the corresponding months folders
inside as well, with each of those month folders containing the 6 files.

The script requires a running instance of chrome with debug commands to connect to in order for
a human to manually circumvent the bot detection puzzles.

pyautogui is used to save the PDFs so chrome must be the active window when the script is running.

For now, make sure the base_download_dir doesn't have any other files in it (folders are fine). This
should be updated in the future for better handling.
'''

import os
import re
import time
import shutil
import glob
import pyautogui
from selenium import webdriver
from bs4 import BeautifulSoup

#Define file paths and directories
url_file_path = "./jaad_urls.txt"
base_download_dir = os.path.expanduser('~/Downloads')
base_target_dir = "./CME_Downloads"

# Create the base target directory if it doesn't exist already
if not os.path.exists(base_target_dir):
    os.makedirs(base_target_dir)

# Helper functions

# Function to remove part identifier from Journal Titles
def remove_part_identifier(title):
    # Define the regex pattern to match "part 1:", "part 2:", "part I:", or "part II:"
    pattern = r'\bpart (1|2|II|I)(:|\.)?\s*'

    # Use re.sub to remove the matched pattern from the title
    title = re.sub(pattern, '', title, flags=re.IGNORECASE)
    # Replace multiple spaces with a single space
    title = re.sub(r'\s+', ' ', title).strip()
    # Replace all instances of " . " with ". "
    title = re.sub(r'\s\.\s', '. ', title)

    #Check if title has more than 6 words
    words = title.split()
    if len(words) > 5:
        title = ' '.join(words[:5])
        title = title.rstrip('.,;!?')
        title += '...'

    return title

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
#
# Using ChromeDriver for a separate instance of debug chrome couldn't get around
# the bot verification when done manually. Work around is to log in and
# handle the verification and then connect to the already running instance of chrome
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#Connect to existing Chrome instance
print("Attempting to connect to chrome")
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get("https://identity.aad.org/?ReturnUrl=%2Felsevier")
print("Attempting to navigate to login page")

print("Log in manually and pass any bot verification as required.")
input("Press Enter to proceed to downloads")

# Parse the URL file
print("Attempting to parse file")
with open(url_file_path, 'r') as file:
    lines = file.readlines()


# Loop through each line in the URL file
for line in lines:
    # Extract the URL, month, and year from the line
    url, date_info = line.strip().split(' for ')
    month, year = date_info.split(' ')
    month_number = get_month_number(month)
    #print(f"URL is {url}, month is {month} and year is {year}")

    # Construct the month-year directory path
    month_year_dir = os.path.join(base_target_dir, year, f"{month_number}_{year} {month}")

    #print(f"month_year_dir directory is {month_year_dir}")

    # Delete the existing month folder and recreate it
    if os.path.exists(month_year_dir):
        shutil.rmtree(month_year_dir)
    os.makedirs(month_year_dir, exist_ok=True)

    # Navigate to the URL
    driver.get(url)
    print(" ")
    print(" ")
    print(" ")
    print(f"Next Journal: {month} {year}")

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

        #Download until we get the 6 we want
        saved_files_count = 0
        i = 0

        exam_count = 1
        answers_count = 1
        retry = 3

        while saved_files_count < 6 and i < len(pdf_links_and_titles): 
            pdf_path, pdf_title = pdf_links_and_titles[i]
            #print(f"PDF URL: {pdf_url}, Title: {pdf_title}")
    
            # Construct the full URL. They all start with the same jaad.org
            pdf_url = "https://www.jaad.org" + pdf_path
    
            #print(f"Opening and downloading PDF {i + 1}: {pdf_title}")
            #print("The corrected URL is: {}".format(pdf_url))
    
            #Navigate to the PDF link to trigger the download
            #print("Attempting to open PDF")
            driver.get(pdf_url)
            print(" ")
    
            # Wait for PDF to open
            time.sleep(2)
    
            # Trigger ctrl+p to save the pdf
            # We use pyautogui because webdriver actions weren't working
            # This requires chrome to be the active window when the script is running
            #print("Printing to save to pdf...")
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(0.4)
            pyautogui.hotkey('enter')
            time.sleep(0.4)
            pyautogui.hotkey('enter')
            time.sleep(1)
    
            # Find the newest downloaded file in the download directory
            # Right now script requires the ~/Download directory to not have any other files
            # to deal with error handling..
            list_of_files = glob.glob(os.path.join(base_download_dir, '*.pdf'))
            if not list_of_files:
                print(f"Error: No PDF file was downloaded for {month} {year}, {pdf_title}.")
                print(f"Retrying {retry} more time(s)")
                retry -= 1
                if retry == 0:
                    i += 1
                    retry = 3
                    print("Couldn't download file after 3 tries, moving to next file")
                continue
            else:
                retry = 3

            latest_file = max(list_of_files, key=os.path.getctime)
    
            #Define new file path
            base_file_name = f"{month} {year} -"

            # Janky Hard coded behavior to pull the PDFs we want.
            # Duaa wants each of the files to be named in a particular way as well.
            # The exan answer pdfs vary, this has been hardcoded for now to cover all cases
            # The actual exam pdfs always contain "CME examination"
            # Assume the first pdf link is part 1. This seems like a safe bet for now
            # If it's not any of the above it's probably the 2nd journal if we've already
            #    downloaded 3-4 files, otherwise it's unknown and flagged for review
            if i == 0:
                pdf_title = remove_part_identifier(pdf_title)
                new_file_name = f"{base_file_name} {pdf_title} part I.pdf"
            elif pdf_title == "PDF" or "Answers to CME examination" in pdf_title or pdf_title == "Supplemental Materials":
                new_file_name = f"{base_file_name} CME exam answers {answers_count}.pdf"
                answers_count += 1
            elif "CME examination" in pdf_title:
                new_file_name = f"{base_file_name} CME examination {exam_count}.pdf"
                exam_count += 1
            elif "Game Changers" in pdf_title: # Skip Game Changers
                i += 1
                os.remove(latest_file) #Delete the downloaded file we are skipping
                continue
            elif i in [3, 4]: #if we're 4th or 5th, prob part 2 if we aren't exam or answers
                # this part is kind of janky, might need to replace
                pdf_title = remove_part_identifier(pdf_title)
                new_file_name = f"{base_file_name} {pdf_title} part II.pdf"
            else: # assume it is part 2 anyways, but flag for review. don't increase saved files count
                print("!!! WARNING UNKOWN FILE !!! Saving anyways, please review!")
                new_file_name = f"PDF {i+1} - {base_file_name} {pdf_title} <<REVIEW.pdf"
                review_path = os.path.join(month_year_dir, "review")
                if not os.path.exists(review_path):
                    with open(review_path, 'w') as file:
                        pass # The 'pass' is a placeholder



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

            # Update counters
            i += 1
            saved_files_count += 1

else:
    print("Script has completed!")

# Keep the browser open for manual inspection
input("Press Enter to finish the program")

# Close the browser
driver.quit()

