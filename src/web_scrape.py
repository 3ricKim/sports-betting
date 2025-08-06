import urllib.request
from bs4 import BeautifulSoup

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)

with urllib.request.urlopen("https://foxphlgambler.iheart.com/content/2024-11-01-saquon-barkley-week-9-preview-vs-the-jaguars/") as response:
    html_bytes = response.read()
    html = html_bytes.decode("utf-8")

soup = BeautifulSoup(html, "html.parser")
# print(soup.get_text())
print(soup.find_all("img"))


# url = "http://image.prntscr.com/image/ynfpUXgaRmGPwj5YdZJmaw.png"
# page = urllib.request.urlopen(url)

# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# print(html)
