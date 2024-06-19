"""
JAAD CME URL Generator

This script generates URLs for JAAD CME articles based on a given range of months and years.
It performs a Google search for each month-year combination and retrieves the top result.
The results are saved to a text file named 'jaad_urls.txt'.

Use in combination with download_cme_pdfs.py to get CME journals, exams, and exam answers.

Usage:
    python cme_urls.py <start_month> <start_year> <end_month> <end_year>

    <start_month> : The starting month (name or number)
    <start_year>  : The starting year (e.g., 2019)
    <end_month>   : The ending month (name or number)
    <end_year>    : The ending year (e.g., 2024)

Example:
    python cme_urls.py January 2019 June 2024
    python cme_urls.py 1 2019 6 2024
"""

import argparse
from googlesearch import search
import datetime

# Define the range of years and months
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# Helper function to convert month input to month number
def get_month_number(month):
    if isinstance(month, int) or month.isdigit():
        return int(month)
    elif isinstance(month, str):
        return months.index(month.capitalize()) + 1
    else:
        raise ValueError("Invalid month input")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate URLs for JAAD CME.')
parser.add_argument('start_month', type=str, help='Start month (name or number)')
parser.add_argument('start_year', type=int, help='Start year (e.g., 2019)')
parser.add_argument('end_month', type=str, help='End month (name or number)')
parser.add_argument('end_year', type=int, help='End year (e.g., 2024)')
args = parser.parse_args()

# Convert month inputs to numbers
start_month_num = get_month_number(args.start_month)
end_month_num = get_month_number(args.end_month)

# File to store the URLs
output_file = "jaad_urls.txt"

# Open the file in write mode
with open(output_file, "w") as file:
    # Loop through each year and month
    for year in range(args.start_year, args.end_year + 1):
        for month in range(1, 13):
            if (year == args.start_year and month < start_month_num) or (year == args.end_year and month > end_month_num):
                continue
            month_name = months[month - 1]
            # Construct the query
            query = f"JAAD {month_name} {year} CME"

            # Perform the Google search and get the first result
            search_results = search(query, num_results=1)

            # Write the result to the file
            for result in search_results:
                file.write(f"{result} for {month_name} {year}\n")
                print(f"{month_name} {year}: {result}")
                break  # Ensure only the top result is considered

print(f"URLs have been saved to {output_file}")
