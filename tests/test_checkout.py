import pytest

from conftest import PAYMENT, SHIPPING
from pages.checkout_page import CompletePage, PaymentPage, ShippingPage
from pages.login_page import LoginPage

BACKPACK = "Sauce Labs Backpack"


def test_checkout_requires_login(app):
    app.open_product(BACKPACK).add_to_cart()
    app.open_cart().proceed_to_checkout()
    assert LoginPage(app.driver).is_displayed()


def test_shipping_fields_are_required(logged_in):
    logged_in.open_product(BACKPACK).add_to_cart()
    logged_in.open_cart().proceed_to_checkout()
    shipping = ShippingPage(logged_in.driver)
    shipping.submit()
    errors = shipping.error_texts()
    assert "Please provide your full name." in errors
    assert "Please provide your address." in errors
    assert "Please provide your city." in errors
    assert shipping.is_displayed()


def test_payment_fields_are_validated(logged_in):
    logged_in.open_product(BACKPACK).add_to_cart()
    logged_in.open_cart().proceed_to_checkout()
    ShippingPage(logged_in.driver).fill(**SHIPPING).submit()
    payment = PaymentPage(logged_in.driver)
    payment.submit()
    assert "Value looks invalid." in payment.error_texts()
    assert payment.is_displayed()


def test_review_total_is_items_plus_delivery(at_review):
    assert at_review.total() == pytest.approx(at_review.item_price() + at_review.delivery_fee())


@pytest.mark.smoke
def test_order_completes_and_cart_resets(at_review):
    at_review.place_order()
    complete = CompletePage(at_review.driver)
    assert complete.heading() == "Checkout Complete"
    catalog = complete.continue_shopping()
    assert catalog.cart_count() == 0


@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, raises=AssertionError, reason="KD-3: review screen shows the full card number")
def test_review_masks_card_number(at_review):
    shown = at_review.shown_card_number().replace(" ", "")
    assert shown != PAYMENT["card_number"]
    assert shown.endswith(PAYMENT["card_number"][-4:])
