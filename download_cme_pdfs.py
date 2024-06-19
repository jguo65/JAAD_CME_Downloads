from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time

# Define your credentials
username = "shzhang49@gmail.com"
password = "zqm3qpu6GBH-zdh@qmx"
print("Login credentials confirmed")

# Set up the Selenium WebDriver with ChromeDriver bundled with Chrome
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
print("Selenium WebDriver confirmed")

# Navigate to the login page
driver.get("https://identity.aad.org/?ReturnUrl=%2Felsevier")
print("Attempting to navigate to login page")

# Give the page some time to load
time.sleep(5)

# Find the username and password fields and enter your credentials
#username_field = driver.find_element(By.NAME, "Username")
#password_field = driver.find_element(By.NAME, "Password")
#username_field.send_keys(username)
#password_field.send_keys(password)

#hardcode login
actions = webdriver.ActionChains(driver)
actions.send_keys(username)
actions.send_keys(Keys.TAB)
actions.send_keys(password)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.RETURN)
actions.perform()
print("Login fields found, attempting to login")

# Give the login process some time to complete
time.sleep(5)

# Verify if login was successful by checking the URL or page content
if "ReturnUrl" not in driver.current_url:
    print("Login successful")
else:
    print("Login failed")

# Navigate to first url
driver.get("https://www.jaad.org/issue/S0190-9622(18)X0014-0")
print("Attempting to get first page")

#After navigating to desired page, give time for page to load
time.sleep(5)

#Parse the page content
soup = BeautifulSoup(driver.page_source, 'html.parser')

#Find all PDF links on the page
all_links = soup.find_all('a', href=True)
print(f"Found {len(all_links)} total links on the page.")

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

    print(f"the url is: {first_pdf_url}")

    # Download the PDF
    response = requests.get(first_pdf_url)

    # Save PDF to curr directory
    with open('pdf_test.pdf', 'wb') as file:
        file.write(response.content)
    
    print(f"Downloaded first PDF as pdf_test.pdf from {first_pdf_url}")

else:
    print("No PDF links found on the page.")

# Keep the browser open for manual inspection
input("Press Enter to close the browser...")

# Close the browser
driver.quit()

