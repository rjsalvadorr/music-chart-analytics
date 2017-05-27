import requests
from bs4 import BeautifulSoup

resp = requests.get("https://tabs.ultimate-guitar.com/m/marvin_gaye/whats_going_on_ver3_crd.htm")

print("Status: " + str(resp.status_code))

pageContent = resp.content
soup = BeautifulSoup(pageContent, "html.parser")

tabContentHtml = soup.select(".js-tab-content")[0]
tabContent = tabContentHtml.get_text()

print(tabContent)
