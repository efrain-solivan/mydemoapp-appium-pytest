from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage, rid


class LoginPage(BasePage):
    HEADING = rid("loginTV")
    USERNAME = rid("nameET")
    PASSWORD = rid("passwordET")
    SUBMIT = rid("loginBtn")

    def is_displayed(self):
        return self.is_present(self.HEADING)

    def login(self, username, password):
        self.find(self.USERNAME)
        if username:
            self.type(self.USERNAME, username)
        if password:
            self.type(self.PASSWORD, password)
        self.hide_keyboard()
        self.tap(self.SUBMIT)
        self._wait_for_outcome()

    def _wait_for_outcome(self):
        """Block until the login settles: an inline error or the catalog."""
        WebDriverWait(self.driver, self.TIMEOUT).until(
            lambda d: self.error_texts() or d.find_elements(*rid("titleTV"))
        )

    def is_logged_in(self):
        """True when the side menu offers Log Out (the app's only login state signal)."""
        menu = self.open_menu()
        logged_in = "Log Out" in menu.item_texts()
        self.driver.back()  # close the drawer
        return logged_in
