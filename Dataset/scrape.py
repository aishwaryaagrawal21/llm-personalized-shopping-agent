import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import time

# Function to download an image and return the file path
def download_image(url, folder, filename):
    if url:
        path = os.path.join(folder, f"{filename}.jpg")
        urllib.request.urlretrieve(url, path)
        return path
    return None

# Set up Selenium WebDriver options
options = webdriver.ChromeOptions()
#options.add_argument('--headless')

# Initialize the WebDriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Path to the CSV file
csv_file_path = '/Users/ameyamorbale/Documents/CMU/Fall_2023/LLM/Project/Dataset/grocery_updated.csv'

# Load the CSV file
df = pd.read_csv(csv_file_path)

# Ensure the Images directory exists
image_dir = '/Users/ameyamorbale/Documents/CMU/Fall_2023/LLM/Project/Dataset/Images'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Add a new column for image paths
df['ImagePath'] = None

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    search_term = row['SKU']  # Replace 'SKU' with your actual column name for search queries
    url = f"https://www.google.com/search?q={search_term}&tbm=isch&tbs=sur:fc&hl=en"

    driver.get(url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)

    img_results = driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]")
    if img_results:
        src = img_results[0].get_attribute('src')
        image_path = download_image(src, image_dir, f"image_{index}")
        df.at[index, 'ImagePath'] = image_path

# Quit the WebDriver
driver.quit()

# Save the updated DataFrame to CSV
df.to_csv(csv_file_path, index=False)
