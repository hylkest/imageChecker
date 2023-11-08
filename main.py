import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin

def get_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def check_broken_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    broken_images = []

    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        img_src = img_tag.get('src')
        absolute_url = urljoin(url, img_src)

        try:
            img_response = requests.get(absolute_url)
            Image.open(BytesIO(img_response.content))
        except Exception as e:
            broken_images.append((absolute_url, str(e)))

    return broken_images

def log_broken_images(broken_images, log_file='test.txt'):
    with open(log_file, 'a') as file:
        for img_url, error_msg in broken_images:
            file.write(f"Broken image found: {img_url} - {error_msg}\n")

def main(sitemap_url):
    urls = get_sitemap_urls(sitemap_url)

    for url in urls:
        print(f"Checking {url} for broken images...")
        broken_images = check_broken_images(url)

        if broken_images:
            print(f"Broken images found on {url}:")
            for img_url, error_msg in broken_images:
                print(f"  {img_url} - {error_msg}")
            log_broken_images(broken_images)
        else:
            print(f"No broken images found on {url}")

if __name__ == "__main__":
    sitemap_url = "https://cssight.com/sitemap.xml"  # Replace with the actual sitemap URL
    main(sitemap_url)
