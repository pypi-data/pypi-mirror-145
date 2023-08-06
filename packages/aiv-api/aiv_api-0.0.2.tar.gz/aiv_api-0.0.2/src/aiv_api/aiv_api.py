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
from aiv_api.convert_df import convert_df
from aiv_api.list_portfolios import list_portfolios
from aiv_api.html_to_df import html_to_df

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class aiv_api():

    def __init__(self):
        self.portfolios = {}

    def login(self, personid, headless=False):
        """ """
        url = "https://secure.aktieinvest.se/login"
        delay = 100
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

        driver.get(url)  # open website

        # Find and click login button
        xpath = '//button[text()="Mobilt BankID"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        # Enter personid
        xpath = '//input[contains(@class, "id-number")]'
        elem = WebDriverWait(driver, 100).until(EC.presence_of_element_located((
                                                By.XPATH, xpath)))
        elem.send_keys(personid)
        elem.submit()

        # Login with bankid
        xpath = '//h3[text()="Mina innehav"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        self.driver = driver
        self.list_portfolios()

    def list_portfolios(self):
        portfolios, tot_val = list_portfolios(self.driver.page_source)

        self.tot_val = tot_val
        self.portfolio_names = portfolios

        return portfolios

    def fetch_portfolio(self):
        """Fetch the portfolio"""
        driver = self.driver
        delay = 100
        self.port_val = 0
        for idx, portfolio in enumerate(self.portfolio_names):
            # Enter portfolio
            xpath = f'//a[text()="{portfolio}"]'
            elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                      By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", elem)

            # Wait for portfolio
            xpath = '//h1[text()="Innehav"]'
            elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                      By.XPATH, xpath)))


            df_converted = html_to_df(driver.page_source)
            self.portfolios[portfolio] = df_converted

            if idx < 2:
                self.port_val = self.port_val + df_converted["Värde"].sum()

            # Go back to prev page
            driver.execute_script("window.history.go(-1)")

        self.cash_val = self.tot_val - self.port_val
        print(f"Fetched self.portfolios: {self.portfolios.keys()}")

    def login_and_fetch(self, personid, headless=False):
        """Convenience function"""
        self.login(personid, headless=headless)
        self.fetch_portfolio()

    def save_csv(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_aiv_{today}.csv"
        self.df.to_csv(filename)

    def save_ascii(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        i = 1
        for key, val in self.portfolios_dict.items():
            filename = f"portfolio_aiv_{today}_{i}"
            with open(f'./{filename}.txt', 'w') as fo:
                fo.write(val.__repr__())
            i = i + 1
