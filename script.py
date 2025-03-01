import requests
import os
import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Tumblr blog URL
blog_url = 'https://theprofoundprogrammer.tumblr.com/'

# Directory to save images and descriptions
save_dir = 'downloaded_images'
os.makedirs(save_dir, exist_ok=True)

# Headers to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# Keep track of downloaded images
downloaded_images = set()

# Function to convert Imgur URLs to correct download format
def fix_imgur_url(imgur_url):
    match = re.match(r'https?://i\.imgur\.com/([a-zA-Z0-9]+)\.(jpg|png|gif)', imgur_url)
    if match:
        image_id = match.group(1)
        return f'https://i.imgur.com/{image_id}.jpeg'
    return imgur_url  # Return original if no match

# Function to download an image
def download_image(url, save_path):
    if url in downloaded_images:
        print(f'Skipping already downloaded: {url}')
        return

    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f'Successfully downloaded: {url}')
            downloaded_images.add(url)  # Track downloaded image
        elif response.status_code == 404:
            print(f'Image not found (404): {url}')
        else:
            print(f'Failed to retrieve ({response.status_code}): {url}')
    except Exception as e:
        print(f'Error downloading {url}: {e}')

# Function to extract image descriptions
def get_image_description(post):
    caption = post.find('div', class_='caption')
    if caption:
        first_p = caption.find('p')
        if first_p:
            return first_p.get_text(strip=True)
    return None  # No description found

# Function to extract Imgur image links and their corresponding descriptions
def extract_imgur_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    imgur_data = {}

    # Find all posts with images
    for post in soup.find_all('li', class_='post photo'):
        img_tag = post.find('img')
        hd_link = post.find('a', string=re.compile(r'\[HD Version\]', re.IGNORECASE))

        if img_tag and hd_link:
            imgur_url = urljoin(blog_url, hd_link.get('href'))
            fixed_url = fix_imgur_url(imgur_url)  # Convert to correct format

            # Get the description
            description = get_image_description(post)

            imgur_data[fixed_url] = description

    return imgur_data

# Function to get the next page URL correctly
def get_next_page_url(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    next_link = soup.find('a', string=re.compile(r'Next »', re.IGNORECASE))

    if next_link:
        next_page_url = urljoin(blog_url, next_link.get('href'))
        return next_page_url
    return None  # No more pages

# Start scraping
current_url = blog_url
while current_url:
    try:
        response = requests.get(current_url, headers=headers)
        if response.status_code == 200:
            page_content = response.text
            imgur_data = extract_imgur_data(page_content)

            # Download each Imgur image and save the description
            for imgur_link, description in imgur_data.items():
                img_name = os.path.basename(imgur_link.split('?')[0])
                img_id = os.path.splitext(img_name)[0]  # Extract image ID without extension
                img_path = os.path.join(save_dir, img_name)
                txt_path = os.path.join(save_dir, f"{img_id}.txt")

                # Download image
                download_image(imgur_link, img_path)

                # Save description if available
                if description:
                    with open(txt_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(description)
                    print(f'Saved description: {txt_path}')
                else:
                    print(f'No description found for {img_name}')

            # Get next page URL
            next_page_url = get_next_page_url(page_content)
            if next_page_url and next_page_url != current_url:
                print(f"Moving to next page: {next_page_url}")
                current_url = next_page_url
                time.sleep(1)  # Be polite to the server
            else:
                print("No more pages found.")
                break
        else:
            print(f'Failed to retrieve page ({response.status_code}): {current_url}')
            break
    except Exception as e:
        print(f'Error processing {current_url}: {e}')
        break

print('HD image extraction and description saving completed.')