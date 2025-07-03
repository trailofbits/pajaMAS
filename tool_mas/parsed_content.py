from bs4 import BeautifulSoup
import re
import os

html_path = os.path.join(os.path.dirname(__file__), "placeholder.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(separator=" ", strip=True)
parsed_content = re.sub(r"\s+", " ", text).strip()
