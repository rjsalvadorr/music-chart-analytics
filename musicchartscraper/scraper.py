import requests
from bs4 import BeautifulSoup

page = requests.get("https://tabs.ultimate-guitar.com/m/marvin_gaye/whats_going_on_ver2_crd.htm")
print("Status: " + str(page.status_code))