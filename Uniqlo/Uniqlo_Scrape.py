from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--incognito")
options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\User\Downloads\chromedriver\chromedriver.exe")

url = "https://www.uniqlo.com/my/store/women-hybrid-down-parka-4202510015.html#colorSelect"
page = driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')
print(soup.prettify())

https://www.youtube.com/watch?v=Z6tmDdrBnpU