from playwright.sync_api import sync_playwright
import time
import requests
import sys

def main(quote_index):

    video_path = f"vids/{quote_index}.mp4"

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        context = browser.contexts[0]
        page = None

        for open_page in context.pages:
            if "instagram" in open_page.url:
                page = open_page
                page.goto("https://www.instagram.com")
                break
        if not page:
            page = context.new_page()
            page.goto("https://www.instagram.com")

        create = page.locator("span", has_text="New post")
        create.click()
        time.sleep(1)

        page.set_input_files("input[type=file]", video_path)

        time.sleep(1)

        page.click("svg[aria-label='Select Crop']")

        time.sleep(1)

        page.click("svg[aria-label='Crop portrait icon']")

        time.sleep(1)

        time.sleep(3)

        next_button = page.get_by_role("button", name="Next")
        next_button.click()

        time.sleep(1)

        next_button = page.get_by_role("button", name="Next")
        next_button.click()

        time.sleep(1)

        share_button = page.get_by_role("button", name="Share")
        share_button.click()

        time.sleep(5)

if __name__ == "__main__":
    main(sys.argv[1])
