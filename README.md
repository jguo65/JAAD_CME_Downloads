Steps to get CME docs

1. Run cme_urls.py with your rage of dates
2. Double check the jaad_urls.txt and fix any bad or incorrect URLs. Sometimes the 2nd page is the 1st result
3. Start an instance of chrome with the proper debug command:
    flatpak run com.google.Chrome --remote-debugging-port=9222 --user-data-dir="/your/path/to/custom_chrome_profile"
    This is subject to change depending on how chrome is installed for you
4. Run downlad_cme_pdfs.py, solve bot verification puzzle and let the magic happen.

