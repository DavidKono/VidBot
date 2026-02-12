from playwright.sync_api import sync_playwright
import time
import requests

folder = "bgs"

def is_vertical(w, h):
    ratio = h/w
    return 1.4 <= ratio <= 2.0

# try get bestquality image
def get_best_url(image):
    srcset = image.get_attribute("srcset")
    if srcset:
        print(srcset.split(",")[-1].split()[0])
        return srcset.split(",")[-1].split()[0]
    src = image.get_attribute("src")
    if src:
        print(src.split(",")[-1].split()[0])
        return src.replace("236x", "originals")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")

    context = browser.contexts[0]
    page = context.pages[0]

    # or keep page open
    # page.goto("https://www.pinterest.com/search/pins/?q=Beautiful%20Nature%20pink&rs=typed")

    time.sleep(3)
    print("ready")

    images = page.query_selector_all("img")    

    urls = []

    for image in images:
        # only check vertical images
        box = image.bounding_box()
        if not box: continue
        if is_vertical(box["width"], box["height"]):
            urls.append(get_best_url(image))

for i, url in enumerate(set(urls)):
    filename = url.split("/")[-1]
    req = requests.get(url, timeout=10)
    with open(f"he/{filename}", "wb") as file:
        file.write(req.content)



