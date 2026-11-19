from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, rid


class Menu(BasePage):
    ITEMS = rid("itemTV")

    def item_texts(self):
        self.find(self.ITEMS)
        return [e.text for e in self.find_all(self.ITEMS)]

    def choose(self, label):
        self.tap((AppiumBy.XPATH, f'//*[@resource-id="{self.ITEMS[1]}" and @text="{label}"]'))

    def go_to_login(self):
        from pages.login_page import LoginPage

        self.choose("Log In")
        return LoginPage(self.driver)

    def go_to_catalog(self):
        from pages.catalog_page import CatalogPage

        self.choose("Catalog")
        return CatalogPage(self.driver).wait_loaded()
