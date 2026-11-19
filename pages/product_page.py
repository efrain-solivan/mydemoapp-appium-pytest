from pages.base_page import BasePage, price_value, rid


class ProductPage(BasePage):
    PRICE = rid("priceTV")
    QUANTITY = rid("noTV")
    PLUS = rid("plusIV")
    MINUS = rid("minusIV")
    ADD_TO_CART = rid("cartBt")

    def wait_loaded(self):
        self.find(self.ADD_TO_CART)
        return self

    def name(self):
        return self.text_of(self.SCREEN_TITLE)

    def price(self):
        return price_value(self.text_of(self.PRICE))

    def quantity(self):
        return int(self.text_of(self.QUANTITY))

    def increase(self, times=1):
        for _ in range(times):
            self.tap(self.PLUS)
        return self

    def decrease(self, times=1):
        for _ in range(times):
            self.tap(self.MINUS)
        return self

    def add_to_cart(self):
        self.tap(self.ADD_TO_CART)
        return self
