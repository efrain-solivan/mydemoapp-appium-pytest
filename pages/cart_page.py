from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage, price_value, rid


class CartPage(BasePage):
    ITEM_TITLES = rid("titleTV")
    PLUS = rid("plusIV")
    REMOVE = rid("removeBt")
    ITEM_COUNT = rid("itemsTV")
    TOTAL = rid("totalPriceTV")
    CHECKOUT = rid("cartBt")
    # The empty-cart view is a separate layout; match its heading by text.
    EMPTY_HEADING = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No Items")')

    def wait_loaded(self):
        """'My Cart' or 'No Items' heading. The checkout button reuses the product
        screen's cartBt id, so acting before this wait can hit the old screen."""
        WebDriverWait(
            self.driver, self.TIMEOUT, ignored_exceptions=(StaleElementReferenceException,)
        ).until(lambda d: d.find_elements(*self.TOTAL) or d.find_elements(*self.EMPTY_HEADING))
        return self

    def item_names(self):
        self.find(self.ITEM_TITLES)
        return [e.text for e in self.find_all(self.ITEM_TITLES)]

    def item_count(self):
        # "2 Items" -> 2
        return int(self.text_of(self.ITEM_COUNT).split()[0])

    def total(self):
        return price_value(self.text_of(self.TOTAL))

    def increase_first_item(self):
        self.tap(self.PLUS)
        return self

    def remove_first_item(self):
        self.tap(self.REMOVE)
        return self

    def is_empty(self):
        return self.is_present(self.EMPTY_HEADING)

    def proceed_to_checkout(self):
        self.tap(self.CHECKOUT)
