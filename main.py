from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import chromedriver_autoinstaller


class QuoteScraper:
    def __init__(self):
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        # Opening login page and entering dummy variables 
        # Same as directly going to 'https://quotes.toscrape.com'

        self.driver.get('https://quotes.toscrape.com/login')

        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        loginButton = self.driver.find_element(By.XPATH, "//*[@value='Login']")

        username.send_keys('a')
        password.send_keys('a')
        loginButton.click()
    
    def getDriverQuotes(self):
        # Helper function to retrieve data from the driver page into the quotes list
        #Setting up BeautifulSoup parser and getting a list of html elements of quotes

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        divs = soup.find_all(itemtype="http://schema.org/CreativeWork")

        for div in divs:
            quoteInfo = {}
            content = div.contents
            quoteInfo['quote'] = content[1].string[1:-1]
            quoteInfo['author'] = content[3].contents[1].string
            quoteInfo['author_link'] = "https://quotes.toscrape.com" + content[3].contents[3]["href"]
            quoteInfo['tags'] = content[5].contents[1]["content"].split(',')
            self.quotes.append(quoteInfo)

    def exportQuotes(self):
        
        self.login()
        self.quotes = []
        self.getDriverQuotes()

        # Getting quotes from second page through the link at the bottom of the page

        page2 = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Next").get_attribute('href')

        self.driver.get(page2)

        self.getDriverQuotes()

        self.driver.quit()

        # Convert data to json and write to file

        json_object = json.dumps(self.quotes, ensure_ascii=False)
        with open("output.json", "w") as file:
            file.write(json_object)

QuoteScraper().exportQuotes()