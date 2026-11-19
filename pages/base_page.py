from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PKG = "com.saucelabs.mydemoapp.android"


def rid(name):
    """Locator for an element of the app under test, by resource-id."""
    return (AppiumBy.ID, f"{PKG}:id/{name}")


def price_value(text):
    """'$ 29.99' -> 29.99"""
    return float(text.replace("$", "").strip())


class BasePage:
    TIMEOUT = 15

    # Header shared by every screen
    MENU = rid("menuIV")
    CART = rid("cartRL")
    CART_BADGE = rid("cartTV")
    SCREEN_TITLE = rid("productTV")

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def tap(self, locator, attempts=3):
        """Click once clickable; retry if the view is re-rendered between find and click."""
        for attempt in range(attempts):
            try:
                WebDriverWait(self.driver, self.TIMEOUT).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                return
            except StaleElementReferenceException:
                if attempt == attempts - 1:
                    raise

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)
        return field

    def text_of(self, locator):
        return self.find(locator).text

    def is_present(self, locator, timeout=5):
        try:
            self.find(locator, timeout)
            return True
        except Exception:
            return False

    def hide_keyboard(self):
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    def scroll_to(self, resource_name):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().resourceId("{PKG}:id/{resource_name}"))',
        )

    def error_texts(self):
        """Visible inline validation messages (the app's ids contain 'Error').
        A native UiSelector instead of XPath: XPath dumps the whole view tree per call."""
        els = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*Error.*")'
        )
        texts = []
        for e in els:
            try:
                if e.text:
                    texts.append(e.text)
            except StaleElementReferenceException:
                pass
        return texts

    # Header actions
    def cart_count(self):
        badges = self.find_all(self.CART_BADGE)
        return int(badges[0].text) if badges and badges[0].text else 0

    def open_cart(self):
        from pages.cart_page import CartPage

        self.tap(self.CART)
        return CartPage(self.driver).wait_loaded()

    def open_menu(self):
        from pages.menu import Menu

        self.tap(self.MENU)
        return Menu(self.driver)
