import pytest

from conftest import LOCKED_USER, VALID_USER
from pages.catalog_page import CatalogPage


@pytest.fixture
def login_page(app):
    return app.open_menu().go_to_login()


@pytest.mark.smoke
def test_valid_user_logs_in(login_page):
    login_page.login(*VALID_USER)
    catalog = CatalogPage(login_page.driver).wait_loaded()
    assert catalog.title() == "Products"
    assert "Log Out" in catalog.open_menu().item_texts()


def test_locked_out_user_is_refused(login_page):
    login_page.login(*LOCKED_USER)
    assert "Sorry this user has been locked out." in login_page.error_texts()
    assert not login_page.is_logged_in()


def test_username_is_required(login_page):
    login_page.login("", VALID_USER[1])
    assert "Username is required" in login_page.error_texts()


def test_password_is_required(login_page):
    login_page.login(VALID_USER[0], "")
    assert "Enter Password" in login_page.error_texts()


@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, raises=AssertionError, reason="KD-1: any password is accepted for a known user")
def test_wrong_password_is_refused(login_page):
    login_page.login(VALID_USER[0], "not-the-password")
    assert not login_page.is_logged_in()


@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, raises=AssertionError, reason="KD-2: an unregistered username is accepted")
def test_unknown_user_is_refused(login_page):
    login_page.login("nobody@example.com", "10203040")
    assert not login_page.is_logged_in()
