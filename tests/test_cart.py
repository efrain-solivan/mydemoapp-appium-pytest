import pytest

BACKPACK = "Sauce Labs Backpack"


@pytest.mark.smoke
def test_add_to_cart_updates_badge(app):
    assert app.cart_count() == 0
    app.open_product(BACKPACK).add_to_cart()
    assert app.cart_count() == 1


def test_quantity_stepper_adds_that_many(app):
    product = app.open_product(BACKPACK).increase(2)
    assert product.quantity() == 3
    product.add_to_cart()
    assert product.cart_count() == 3


def test_zero_quantity_disables_add_to_cart(app):
    product = app.open_product(BACKPACK).decrease(2)
    assert product.quantity() == 0  # floors at zero, never negative
    assert not product.find(product.ADD_TO_CART).is_enabled()
    assert product.cart_count() == 0


def test_cart_shows_item_and_total(app):
    price = app.open_product(BACKPACK).add_to_cart().price()
    cart = app.open_cart()
    assert cart.item_names() == [BACKPACK]
    assert cart.item_count() == 1
    assert cart.total() == price


def test_cart_total_follows_quantity(app):
    price = app.open_product(BACKPACK).add_to_cart().price()
    cart = app.open_cart().increase_first_item()
    assert cart.item_count() == 2
    assert cart.total() == pytest.approx(price * 2)


def test_remove_item_empties_cart(app):
    app.open_product(BACKPACK).add_to_cart()
    cart = app.open_cart().remove_first_item()
    assert cart.is_empty()
    assert cart.cart_count() == 0
