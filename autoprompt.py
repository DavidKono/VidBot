from playwright.sync_api import sync_playwright
import json
import time

prompt_text = open("prompt.txt", encoding="utf-8").read()
json_file_text = open("quotes.json").read()

if not prompt_text or not json_file_text:
    FileNotFoundError("couldnt get text from prompt.txt or quotes.json")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")

    context = browser.contexts[0]
    page = None

    for open_page in context.pages:
        if "grok" in open_page.url:
            page = open_page
            break
    if not page:
        page = context.new_page()
        page.goto("https://www.grok.com")

    time.sleep(3)
    print("ready")

    input_box = page.locator("div[contenteditable='true']").first
    time.sleep(3)
    print("found text box")

    input_box.fill(prompt_text + json_file_text)
    time.sleep(3)
    
    input_box.press("Enter")
    print("entered text")

    time.sleep(120)

    # just get last message
    messages = page.locator("div.response-content-markdown p") 
    response = messages.nth(-1).inner_text()
    
    print("grok says: \n", response)

    browser.close()

# write back quotes into quotes.json
new_quotes = json.loads(response)
old_quotes = json.loads(json_file_text)

for quote in new_quotes:
    print(quote)
    if quote not in old_quotes:
        old_quotes.append(quote)

with open("quotes.json", "w", encoding="utf-8") as file:
    json.dump(old_quotes, file, indent=4, ensure_ascii=False)