import json
import sys

quote_index = int(open("quotes_i.json").read())

print(quote_index)

quotes_raw = open("quotes.json").read()
quotes = json.loads(quotes_raw)

for quote in quotes:
    print(quote)

num_quotes = len(quotes)
print(num_quotes)

# get more quotes if missing
if num_quotes < (quote_index + 10):
    with open("autoprompt.py") as file:
        code = file.read()
        exec(code)

# create video
sys.argv = ["vidbot.py", quote_index]
with open("vidbot.py") as file:
    code = file.read()
    exec(code)

# post video
sys.argv = ["poster.py", quote_index]
with open("poster.py") as file:
    code = file.read()
    exec(code)

# update index
quote_index += 1
with open("quotes_i.json", "w", encoding="utf-8") as file:
    json.dump(quote_index, file, ensure_ascii=False)









