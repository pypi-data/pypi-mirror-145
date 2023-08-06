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
from nda_api.html_to_df import html_to_df

class nda_api():

    def __init__(self):
        pass

    def login(self, headless=True):
        """ """
        url = "https://investor.nordea.se"
        delay = 10
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
        time.sleep(1)

        # Find and click login button
        xpath = '//span[text()="Logga in"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(1)

        # Find and click ok button
        xpath = '//button[text()="OK"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        # Login with bankid
        xpath = '//span[@id="7f"]'
        elem = WebDriverWait(driver, 100).until(EC.presence_of_element_located((
                                                By.XPATH, xpath)))

        self.driver = driver

    def fetch_portfolio(self):
        """Fetch the portfolio"""
        driver = self.driver
        delay = 100
        xpath = '//span[@id="7f"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        self.tot_val = float(elem.text.replace(",", ".").replace(" ", ""))

        xpath = '//span[text()="Mina investeringar"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        time.sleep(1)
        df = html_to_df(self.driver.page_source)

        self.df = df
        self.port_val = df["Värde"].sum()
        self.cash_val = self.tot_val - self.port_val

        self.portfolios = {"all": df}
        print(f"Fetched self.portfolios: {self.portfolios.keys()}")

        return df

    def login_and_fetch(self, headless=False):
        """Convenience function"""
        self.login(headless=headless)
        self.fetch_portfolio()

    def save_csv(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_nda_{today}.csv"
        self.df.to_csv(filename)

    def save_ascii(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_nda_{today}"
        with open(f'./{filename}.txt', 'w') as fo:
            fo.write(self.df.__repr__())

    def convert_to_std_format(self):
        """ """
        for portfolio, df in self.portfolios.items():
            self.portfolios[portfolio + "_std"] = convert_nda_std(df)
