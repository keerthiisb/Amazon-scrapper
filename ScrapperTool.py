import getpass
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import random
import pickle

# 🔒 Password Protection
PASSWORD = "scrap916"

user_input = getpass.getpass("Enter password to run the script: ")

if user_input != PASSWORD:
    print("Incorrect password! Exiting...")
    exit()

# Path to msedgedriver.exe and chromedriver.exe - update this if necessary
msedgedriver_path = r"C:\webdriver\msedgedriver.exe"
chromedriver_path = r"C:\webdriver\chromedriver.exe"

# Amazon base URL
amazon_base_url = "https://www.amazon.in/dp/"

# Ask the user to choose which browser to use
browser_choice = input("Choose browser (chrome/edge): ").lower()

# Ask user for number of workers and ASINs per worker
num_workers = int(input("Enter the number of workers: "))
asins_per_worker = int(input("Enter the number of ASINs each worker should process: "))

# Function to initialize the selected WebDriver
def get_driver():
    if browser_choice == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        service = ChromeService(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser_choice == "edge":
        edge_options = Options()
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--start-maximized")
        service = Service(msedgedriver_path)
        driver = webdriver.Edge(service=service, options=edge_options)
    else:
        print("Invalid choice! Exiting...")
        exit()
    driver.set_page_load_timeout(120)  # Increase timeout to 120 seconds
    return driver

# Function to check if CAPTCHA is present
def is_captcha_present(driver):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#captchacharacter")))
        print("CAPTCHA detected! Skipping this page...")
        return True
    except (NoSuchElementException, TimeoutException):
        return False

# Function to extract product details using an existing browser instance
def extract_product_details_with_existing_driver(driver, asin):
    url = amazon_base_url + asin

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "productTitle")))
    except (TimeoutException, WebDriverException):
        print(f"Timeout or connection error while loading {url}")
        return {"ASIN": asin, "Title": "Timeout/Error", "URL": url}

    if is_captcha_present(driver):
        return {"ASIN": asin, "Title": "CAPTCHA Found", "URL": url}

    product_details = {"ASIN": asin, "URL": url}

    # Extract product title
    try:
        product_details["Title"] = driver.find_element(By.ID, "productTitle").text.strip()
    except NoSuchElementException:
        product_details["Title"] = "Not Found"

    # Extract product images
    try:
        images = driver.find_elements(By.CSS_SELECTOR, "img[data-a-image-name]")
        for i, img in enumerate(images[:5]):
            product_details[f"Image URL {i+1}"] = img.get_attribute("src")
    except NoSuchElementException:
        pass

    # Extract product details under Technical Details
    try:
        technical_details_section = driver.find_element(By.ID, "productDetails_techSpec_section_1")
        rows = technical_details_section.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                header = row.find_element(By.TAG_NAME, "th").text.strip()
                value = row.find_element(By.TAG_NAME, "td").text.strip()
                product_details[header] = value
            except NoSuchElementException:
                continue
    except NoSuchElementException:
        pass

    # Extract product description
    try:
        description_section = driver.find_element(By.ID, "productDescription")
        product_details["Product Description"] = description_section.text.strip()
    except NoSuchElementException:
        pass

    # Extract "About This Item" section line by line
    try:
        about_section = driver.find_element(By.ID, "feature-bullets")
        about_items = about_section.find_elements(By.TAG_NAME, "li")
        count = 1
        for item in about_items:
            text = item.text.strip()
            if text:
                product_details[f"About Item {count}"] = text
                count += 1
    except NoSuchElementException:
        pass

    time.sleep(random.uniform(5, 10))  # Increased random delay to avoid detection
    return product_details

# Function to save progress to a file (backup)
def save_progress(scraped_data, index):
    with open("scraped_data_backup.pkl", "wb") as f:
        pickle.dump({"data": scraped_data, "index": index}, f)

# Function to load progress from the backup file
def load_progress():
    if os.path.exists("scraped_data_backup.pkl"):
        with open("scraped_data_backup.pkl", "rb") as f:
            return pickle.load(f)
    return None

# Function to scrape ASINs assigned to a worker without closing the browser
def worker_task(asins_chunk):
    driver = get_driver()  # Initialize a single browser instance for the worker

    scraped_data = []
    for asin in asins_chunk:
        result = extract_product_details_with_existing_driver(driver, asin)
        scraped_data.append(result)
    
    driver.quit()  # Close browser after all assigned ASINs are completed
    return scraped_data

# Function to scrape ASINs with multi-threading
def scrape_asins(asins):
    scraped_data = []
    start_index = 0

    # Check if we have a saved progress
    progress = load_progress()
    if progress:
        scraped_data = progress["data"]
        start_index = progress["index"]

    asins = asins[start_index:]
    
    # Split ASINs into chunks for each worker
    asin_chunks = [asins[i:i+asins_per_worker] for i in range(0, len(asins), asins_per_worker)]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(worker_task, asin_chunks)
    
    # Combine all results
    for result in results:
        scraped_data.extend(result)
    
    return scraped_data

# Read the input Excel file with ASINs
input_file = "input.xlsx"
if not os.path.exists(input_file):
    print("File not found! Check the file path.")
else:
    df = pd.read_excel(input_file)
    asins = df['ProductASIN'].tolist()

    # Scrape product data from all ASINs
    scraped_data = scrape_asins(asins)

    # Convert the data to a DataFrame and save to an output CSV file
    output_file = "output.csv"
    pd.DataFrame(scraped_data).to_csv(output_file, index=False)

    print("Scraping complete. Check the output.csv file.")
