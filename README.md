# The Profound Programmer

A website that displays programming-related content scraped from the "The Profound Programmer" Tumblr blog.

## Project Overview

This project creates a simple, browsable gallery of programming-related images and content sourced from The Profound Programmer Tumblr blog. It consists of:

- A Python script for scraping and downloading images from the Tumblr blog
- JavaScript functionality to manage and display the image data
- A responsive web interface for browsing the content

The site allows programmers to enjoy and share programming humor, insights, and wisdom in a clean, accessible format.

## Installation

### Prerequisites

- Python 3.6 or higher
- A modern web browser
- Internet connection (for initial setup and content updates)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/the-profound-programmer.git
   cd the-profound-programmer
   ```

2. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the image downloader script to fetch content:
   ```
   python script.py
   ```
   This will download images from the Tumblr blog to the `downloaded_images` directory.

4. Generate the image list file:
   ```
   node generate-image-list.js
   ```
   This will create/update the `image-list.js` file with metadata about the downloaded images.

## Usage

### Updating Content

To update the site with new content from the Tumblr blog:

1. Run the Python script again:
   ```
   python script.py
   ```

2. Regenerate the image list:
   ```
   node generate-image-list.js
   ```

### Viewing the Website

Simply open the `index.html` file in a web browser:

```
open index.html  # macOS
# or
explorer.exe index.html  # Windows
# or
xdg-open index.html  # Linux
```

Alternatively, you can serve the files using a local web server:

```
python -m http.server
```

Then visit `http://localhost:8000` in your web browser.

## Project Structure

- `script.py` - Python script for downloading images from the Tumblr blog
- `requirements.txt` - Python dependencies
- `generate-image-list.js` - JavaScript script that generates metadata for downloaded images
- `image-list.js` - Contains the array of image data used by the website
- `index.html` - The main HTML file that displays the content
- `downloaded_images/` - Directory containing all downloaded images from the Tumblr blog

## License

[MIT License](LICENSE)

## Acknowledgements

- Content sourced from The Profound Programmer Tumblr blog
- Built with vanilla JavaScript, HTML, and CSS

