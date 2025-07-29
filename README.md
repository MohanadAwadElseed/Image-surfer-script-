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
## 🚀 How to Use
```bash
python image_scraper.py
```
-The script will ask for:

-Website URL (e.g., https://example.com)

-Output folder name (or press Enter for default: downloaded_images)




## 🧰 Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver (installed and in PATH or specify manually)





Install required packages:
```bash
pip install selenium requests
```


