import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import re


def setup_driver():
    """Set up Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-images")  # Don't load images in browser (we'll get URLs only)

    # You may need to specify the path to your ChromeDriver
    # service = Service("/path/to/chromedriver")
    # driver = webdriver.Chrome(service=service, options=chrome_options)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def download_image(url, folder_path, filename):
    """Download a single image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False


def get_images_from_website(website_url, output_folder="downloaded_images"):
    """Main function to extract and download all images from a website"""

    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    driver = setup_driver()

    try:
        print(f"Loading website: {website_url}")
        driver.get(website_url)

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Scroll to load lazy-loaded images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Find all image elements
        img_elements = driver.find_elements(By.TAG_NAME, "img")

        # Also check for images in CSS backgrounds
        elements_with_bg = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image')]")

        image_urls = set()  # Use set to avoid duplicates

        # Extract image URLs from img tags
        for img in img_elements:
            src = img.get_attribute("src")
            data_src = img.get_attribute("data-src")  # For lazy-loaded images

            for url in [src, data_src]:
                if url:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(website_url, url)
                    if absolute_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')):
                        image_urls.add(absolute_url)

        # Extract background images from CSS
        for element in elements_with_bg:
            style = element.get_attribute("style")
            if "background-image" in style:
                # Extract URL from background-image: url(...)
                match = re.search(r'background-image:\s*url\(["\']?(.*?)["\']?\)', style)
                if match:
                    bg_url = match.group(1)
                    absolute_url = urljoin(website_url, bg_url)
                    if absolute_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')):
                        image_urls.add(absolute_url)

        print(f"Found {len(image_urls)} unique images")

        # Download each image
        downloaded_count = 0
        for i, img_url in enumerate(image_urls, 1):
            try:
                # Generate filename from URL
                parsed_url = urlparse(img_url)
                filename = os.path.basename(parsed_url.path)

                # If no filename in URL, generate one
                if not filename or '.' not in filename:
                    extension = '.jpg'  # default extension
                    filename = f"image_{i}{extension}"

                # Sanitize filename
                filename = sanitize_filename(filename)

                # Add counter if filename already exists
                base_name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(output_folder, filename)):
                    filename = f"{base_name}_{counter}{ext}"
                    counter += 1

                if download_image(img_url, output_folder, filename):
                    downloaded_count += 1

                # Small delay to be respectful to the server
                time.sleep(0.5)

            except Exception as e:
                print(f"Error processing image {i}: {str(e)}")

        print(f"\nDownload complete!")
        print(f"Successfully downloaded {downloaded_count} out of {len(image_urls)} images")
        print(f"Images saved to: {os.path.abspath(output_folder)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    # Get website URL from user
    website_url = input("Enter the website URL: ").strip()

    # Validate URL
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url

    # Optional: custom output folder
    output_folder = input("Enter output folder name (press Enter for 'downloaded_images'): ").strip()
    if not output_folder:
        output_folder = "downloaded_images"

    # Run the image downloader
    get_images_from_website(website_url, output_folder)
