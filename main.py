from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import xmlrunner
from ddt import ddt, data, unpack


@ddt
class TestPopUpWindow(unittest.TestCase):
    def setUp(self):
        # browser init
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=chrome_options)

        # common buttons in pages
        self.send_button_ua_xpath = "//a[text()='Надіслати заявку']"
        self.send_button_ru_xpath = "//a[text()='Отправить заявку']"
        self.pop_up_title_ua_xpath = "//div[@class='pop-up-content-main-form']/div[text()='Отримати консультацію']"
        self.pop_up_title_ru_xpath = "//div[@class='pop-up-content-main-form']/div[text()='Получить консультацию']"
        self.close_pop_up_ua_button_xpath = (
            "//div[@class='pop-up-content-main-form']/../a[@class='close-pop-up w-inline-block']"
        )
        self.close_pop_up_ru_button_xpath = (
            "//div[@class='pop-up-content-main-form']/a[@class='close-pop-up w-inline-block']"
        )
        # time to wait pop up window
        self.delay = 2

    # urls for tests
    main_url_ua = "https://netpeak.ua/"
    main_url_ru = "https://netpeak.ua/ru"
    seo_url_ua = "https://netpeak.ua/ua/services/seo/"
    seo_url_ru = "https://netpeak.ua/ru/services/seo/"
    smm_url_ua = "https://netpeak.ua/ua/services/smm/"
    smm_url_ru = "https://netpeak.ua/ru/services/smm/"
    email_url_ua = "https://netpeak.ua/ua/services/email/"
    email_url_ru = "https://netpeak.ua/ru/services/email/"
    ppc_url_ua = "https://netpeak.ua/ua/services/ppc/"
    ppc_url_ru = "https://netpeak.ua/ru/services/ppc/"

    def check_pop_up(self, url: str, lang: str):
        self.driver.get(url)
        if lang == "ua":
            send_button_xpath = self.send_button_ua_xpath
            pop_up_title_xpath = self.pop_up_title_ua_xpath
            close_pop_up_button_xpath = self.close_pop_up_ua_button_xpath
        elif lang == "ru":
            send_button_xpath = self.send_button_ru_xpath
            pop_up_title_xpath = self.pop_up_title_ru_xpath
            close_pop_up_button_xpath = self.close_pop_up_ru_button_xpath
        else:
            # not used, only for debug
            send_button_xpath = ""
            pop_up_title_xpath = ""
            close_pop_up_button_xpath = ""

        # find all buttons in page
        buttons = WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_all_elements_located((By.XPATH, send_button_xpath)))

        for button in buttons:
            if not button.is_displayed():
                break

            button.click()
            # wait for pop up window is appeared
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, pop_up_title_xpath)))

            # find and press close button
            close_button = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, close_pop_up_button_xpath)))
            close_button.click()
        # close browser
        self.driver.close()

    @data(
        [main_url_ua, "ua"],
        [main_url_ru, "ru"],
        [seo_url_ua, "ua"],
        [seo_url_ru, "ru"],
        [smm_url_ua, "ua"],
        [smm_url_ru, "ru"],
        [email_url_ua, "ua"],
        [email_url_ru, "ru"],
        # [ppc_url_ua, "ua"],
        # [ppc_url_ru, "ru"],
    )
    @unpack
    def test_pages(self, url, lang):
        self.check_pop_up(url, lang)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test_result'))
