import os
import time
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException

from pages.base_page import PKG
from pages.catalog_page import CatalogPage
from pages.checkout_page import PaymentPage, ReviewPage, ShippingPage

ROOT = Path(__file__).parent
APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
APK = Path(os.getenv("APP_PATH", ROOT / "apps" / "mda.apk")).resolve()
REPORTS = ROOT / "reports"

# Demo users the app lists on its own login screen
VALID_USER = ("bod@example.com", "10203040")
LOCKED_USER = ("alice@example.com", "10203040")

SHIPPING = dict(
    full_name="Efrain Tester",
    address1="1 Main St",
    city="Denver",
    zip="80202",
    country="United States",
)
# Published Visa test number; the app has no payment backend
PAYMENT = dict(name="Efrain Tester", card_number="4111111111111111", expiration="0330", cvv="123")


@pytest.fixture(scope="session")
def driver():
    if not APK.exists():
        pytest.exit(f"APK not found at {APK}. Download it first (see README).", 2)
    options = UiAutomator2Options()
    options.app = str(APK)
    options.app_wait_activity = "*"
    options.no_reset = True  # state is reset per test by the `app` fixture
    options.auto_grant_permissions = True
    options.adb_exec_timeout = 60_000
    options.uiautomator2_server_install_timeout = 120_000
    options.new_command_timeout = 300
    drv = webdriver.Remote(APPIUM_URL, options=options)
    # UiAutomator2 waits up to 10 s for the UI to go idle before every command, and an
    # emulator that never reports idle stalls the session. The explicit waits in the
    # page objects already handle readiness.
    drv.update_settings({"waitForIdleTimeout": 100})
    yield drv
    drv.quit()


def _wait_for_catalog(drv, timeout=30):
    """Wait for the product list, tapping OK on the system dialog that 16 KB page-size
    images (Android 15+) show a moment after launch. Android 12 in CI never shows it."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if drv.find_elements(*CatalogPage.TITLES):
            # the dialog can still arrive just after the list renders
            time.sleep(1)
            if not drv.find_elements(AppiumBy.ID, "android:id/button1"):
                return CatalogPage(drv)
        for button in drv.find_elements(AppiumBy.ID, "android:id/button1"):
            try:
                button.click()
            except StaleElementReferenceException:
                pass  # closed on its own before the tap
        time.sleep(0.5)
    return CatalogPage(drv).wait_loaded()


@pytest.fixture
def app(driver):
    """Fresh app state for every test: stop, wipe data, relaunch on the catalog."""
    driver.terminate_app(PKG)
    driver.execute_script("mobile: clearApp", {"appId": PKG})
    driver.activate_app(PKG)
    return _wait_for_catalog(driver)


@pytest.fixture
def logged_in(app):
    app.open_menu().go_to_login().login(*VALID_USER)
    return CatalogPage(app.driver).wait_loaded()


@pytest.fixture
def at_review(logged_in):
    """Logged-in user with one Backpack in the cart, shipping and payment filled."""
    logged_in.open_product("Sauce Labs Backpack").add_to_cart()
    logged_in.open_cart().proceed_to_checkout()
    ShippingPage(logged_in.driver).fill(**SHIPPING).submit()
    PaymentPage(logged_in.driver).fill(**PAYMENT).submit()
    return ReviewPage(logged_in.driver).wait_loaded()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "driver" in item.fixturenames:
        drv = item.funcargs.get("driver")
        if drv is not None:
            REPORTS.mkdir(exist_ok=True)
            drv.save_screenshot(str(REPORTS / f"{item.name}.png"))
