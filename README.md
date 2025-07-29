# 🖼️ Website Image Scraper with Selenium & Requests

This Python script scrapes and downloads all images from a given website — including both visible images (`<img>` tags) and CSS background images — and saves them locally into a folder. It uses Selenium for browser automation and Requests for fast image downloading.

---

## 📦 Features

- ✅ Extracts all `<img>` and background-image URLs
- ✅ Handles lazy-loaded images (e.g., `data-src`)
- ✅ Converts relative URLs to absolute
- ✅ Skips duplicates automatically
- ✅ Downloads all common image formats (.jpg, .png, .gif, .webp, etc.)
- ✅ Headless Chrome browser support
- ✅ Option to set custom output folder

---

## 🧰 Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver (installed and in PATH or specify manually)

🚀 How to Use
bash
Copy code
python image_scraper.py
The script will ask for:

Website URL (e.g., https://example.com)

Output folder name (or press Enter for default: downloaded_images)

📁 Output
All downloaded images will be saved in the selected folder with sanitized filenames to avoid OS errors.

🛠 Configuration
If ChromeDriver is not in your system path, uncomment and update this line in the code:

python
Copy code
# service = Service("/path/to/chromedriver")
# driver = webdriver.Chrome(service=service, options=chrome_options)
🛡️ Notes
Be respectful when scraping — avoid overloading servers.

Some websites use advanced anti-bot mechanisms (e.g., JavaScript rendering, Cloudflare), which may block automated scraping.

This script is for educational and personal use only.




Install required packages:
```bash
pip install selenium requests



