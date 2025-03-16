# Amazon-scrapper
Amazon Product Scraper is an automation tool built using Python, Selenium, and Pandas to extract product details from Amazon based on ASINs. The scraper supports multi-threading, CAPTCHA detection, and error handling for seamless execution.

Introduction

The Amazon Product Scraper is a powerful Python-based automation tool designed to extract detailed product information from Amazon using Selenium WebDriver and Pandas. It efficiently scrapes multiple product pages based on ASINs (Amazon Standard Identification Numbers) and stores the extracted data in a structured format for analysis or catalog management.This project is designed with multi-threading capabilities to improve speed and efficiency, ensuring multiple ASINs are processed simultaneously. Additionally, it includes CAPTCHA detection, error handling, and automatic progress saving to ensure robust and uninterrupted execution.This scraper can be highly useful for e-commerce businesses, data analysts, researchers, and catalog management professionals who need to automate data collection from Amazon.

Key Features

Automated Data Extraction – Retrieves key product details such as title, images, technical specifications, descriptions, and bullet points.
Multi-threading Support – Enables concurrent execution of multiple ASIN scrapes to significantly improve speed.
CAPTCHA Detection & Handling – Automatically detects CAPTCHA challenges and skips blocked pages to prevent script failure.
Error Handling & Timeout Management – Ensures smooth execution even when encountering errors such as missing elements or slow page loads.
Automatic Progress Saving – If the script is interrupted, it resumes from the last processed ASIN using pickle.
Customizable WebDriver Support – Allows users to choose between Chrome or Edge WebDriver for scraping.
Flexible Input & Output Format – Reads ASINs from an Excel file (input.xlsx) and saves the extracted data into CSV format (output.csv).
Human-like Behavior Simulation – Implements randomized delays to avoid detection by Amazon's anti-bot mechanisms.

Technologies Used

Python – Used for scripting and automation.
Selenium WebDriver – Automates browser interactions for web scraping.
Pandas – Processes and structures extracted data efficiently.
Multi-threading (ThreadPoolExecutor) – Allows multiple ASINs to be scraped simultaneously, improving speed.
CAPTCHA Detection & Error Handling – Ensures scraping is not disrupted by unexpected errors.
CSV & Excel Handling (pandas & openpyxl) – Reads ASINs from Excel and saves output in a structured CSV file.

Output Explanation

Once the Amazon Product Scraper completes execution, it generates an output CSV file (output.csv) that contains structured product data extracted from Amazon based on the given ASINs.

Conclusion

Key Takeaways from the Project
Efficient Data Extraction
The scraper successfully extracts detailed product information from Amazon and organizes it into a structured CSV file, making it easy to analyze or use for catalog management.

Scalability and Speed Improvement
By implementing multi-threading, the scraper processes multiple ASINs in parallel, reducing execution time by up to 80 percent compared to sequential scraping.

Automation for E-commerce and Data Analytics
This project automates product data collection, reducing manual effort for businesses, researchers, and data analysts working with e-commerce datasets.

Fault Tolerance and Reliability
With automatic progress saving, the scraper resumes from the last scraped ASIN if interrupted, ensuring data loss is minimized.

Bypassing Challenges (CAPTCHA and Timeouts)
The scraper detects and skips CAPTCHA pages and includes error handling to manage timeouts and missing data, ensuring smooth execution.

