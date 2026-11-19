import time

import pytest

from pages.base_page import PKG
from pages.product_page import ProductPage


@pytest.mark.smoke
def test_catalog_lists_products_with_prices(app):
    products = app.visible_products()
    assert app.title() == "Products"
    assert len(products) >= 2
    assert all(name and price > 0 for name, price in products)


def test_default_order_starts_with_backpack(app):
    assert app.visible_products()[0] == ("Sauce Labs Backpack", 29.99)


@pytest.mark.parametrize(
    "option, key, reverse",
    [
        ("name_asc", lambda p: p[0], False),
        ("name_desc", lambda p: p[0], True),
        ("price_asc", lambda p: p[1], False),
        ("price_desc", lambda p: p[1], True),
    ],
    ids=["name-asc", "name-desc", "price-asc", "price-desc"],
)
def test_sort_orders_visible_products(app, option, key, reverse):
    products = app.sort_by(option).visible_products()
    assert products == sorted(products, key=key, reverse=reverse)


def test_product_detail_matches_catalog_card(app):
    # First card: fully on screen at any resolution (the second, green one is KD-4)
    name, price = app.visible_products()[0]
    product = app.open_product(name)
    assert product.name() == name
    assert product.price() == price


@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="KD-4: opening the green backpack crashes the app "
    "(NullPointerException, ProductCatalogFragment.java:156)",
)
def test_green_backpack_opens_without_crash(app):
    names = [n for n, _ in app.visible_products()]
    app.find_all(app.IMAGES)[names.index("Sauce Labs Backpack (green)")].click()
    time.sleep(3)  # the one fixed wait in the suite: a crash has no element to wait for
    # 4 = RUNNING_IN_FOREGROUND; after the crash the launcher is in front
    assert app.driver.query_app_state(PKG) == 4
    assert app.driver.find_elements(*ProductPage.ADD_TO_CART)
