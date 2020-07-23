from selenium import webdriver


class UiAuto:
    def __init__(self, headers: list = None):
        if headers is None:
            headers = []
        self.options = webdriver.ChromeOptions()
        self.driver_path = r'E:\迅雷下载\chromedriver.exe'
        for header in headers:
            self.options.add_argument(header)
        self.browser = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.options)
        self.browser.implicitly_wait(5)

    def connect(self, domain):
        self.browser.get(domain)
        self.browser.maximize_window()

    def quit(self):
        self.browser.quit()

    def click(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()

    def input(self, xapth, text):
        pass

    def get_context(self, xpath):
        return self.browser.find_element_by_xpath(xpath).text

    def get_contents(self, xpath):
        pass

    @staticmethod
    def from_name_click(name, driver: webdriver.Chrome, xpath='/html/body'):
        elements = driver.find_elements_by_xpath(xpath)
        for element in elements:
            if name in element.text:
                element.click()
                return 1
        return 0

    def choice_date(self, *date):
        time, unit = date
        self.browser.find_element_by_xpath('//*[@id="home"]/div/div[1]/div[2]/div/div[2]').click()
        if unit == '日':
            self.browser.find_elements_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div')
        elif unit == '周':
            self.browser.find_element_by_xpath('//*[@id="tabtime"]/div[2]').click()
            self.from_name_click('25周', driver=self.browser,
                                 xpath='//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div')
        elif unit == '月':
            self.browser.find_element_by_xpath('')
        elif unit == '年':
            self.browser.find_element_by_xpath('')
        else:
            self.browser.find_element_by_xpath('')


if __name__ == '__main__':
    # url = "https://bi.test.laiyifen.com/tianpan/?barhidden=true"
    url = "https://bi.test.laiyifen.com/tianpan/?barhidden=true#/takeoutcommunity"
    a = UiAuto()
    a.connect(url)
    # paid_amount = a.get_xpath('//*[@id="home"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div')
    a.choice_date('27', '周')
    a.quit()
