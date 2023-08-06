""" """
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from datetime import datetime
from non_api.html_to_df import html_to_df


class non_api():

    def __init__(self):
        pass

    def login(self, headless=True):
        """ """
        url = "https://www.nordnet.se/loggain"
        delay = 10
        # Init webdriver
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_argument("--start-maximized")

        try:
            s = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s, options=options)
        except Exception as e:
            print(e)
            gChromeOpts = webdriver.ChromeOptions()
            gChromeOpts.add_argument("window-size=19201480")
            gChromeOpts.add_argument("distable-dev-shm-usage")
            driver = webdriver.chrome(chrome_options=gChromeOpts,
                                      executable_path=ChromeDriverManager().install())

        # Open the website
        driver.get(url)

        # Find and click login buttonpip install html5lip install html5libb
        xpath = '//div[text()="Mobilt BankID"]'
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                     By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", element)

        xpath = '//span[text()="Min ekonomi"]'
        element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((
                                                     By.XPATH, xpath)))

        self.driver = driver

    def list_portfolios(self):
        pass

    def fetch_portfolio(self):
        """Fetch the portfolio"""
        # Login with bankid
        driver = self.driver
        delay = 10
        driver.get("https://www.nordnet.se/oversikt/konto/3")

        xpath = '//h2[text()="Eget kapital"]'
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                     By.XPATH, xpath)))

        time.sleep(2)
        xpath = '//*[contains(text(),"SEK")]'
        element = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((
                                                     By.XPATH, xpath)))

        df, tot_val = html_to_df(driver.page_source)
        self.tot_val = tot_val
        self.port_val = df["Värde SEK"].sum()
        self.cash_val = self.tot_val - self.port_val
        self.df = df
        self.portfolios = {}
        self.portfolios["kf"] = self.df

    def list_portfolios(self):
        pass

    def login_and_fetch(self, headless=False):
        """Convenience"""
        self.login(headless=headless)
        self.fetch_portfolio()

    def save_csv(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_non_{today}.csv"
        self.df.to_csv(filename)

    def save_ascii(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_non_{today}"
        with open(f'./{filename}.txt', 'w') as fo:
            fo.write(self.df.__repr__())
