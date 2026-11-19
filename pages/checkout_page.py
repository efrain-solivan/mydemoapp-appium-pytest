from pages.base_page import BasePage, price_value, rid


class ShippingPage(BasePage):
    FIELDS = {
        "full_name": rid("fullNameET"),
        "address1": rid("address1ET"),
        "address2": rid("address2ET"),
        "city": rid("cityET"),
        "state": rid("stateET"),
        "zip": rid("zipET"),
        "country": rid("countryET"),
    }
    TO_PAYMENT = rid("paymentBtn")

    def is_displayed(self):
        return self.is_present(self.FIELDS["full_name"])

    def fill(self, **values):
        for key, value in values.items():
            self.type(self.FIELDS[key], value)
        self.hide_keyboard()
        return self

    def submit(self):
        self.tap(self.TO_PAYMENT)


class PaymentPage(BasePage):
    HEADING = rid("enterPaymentMethodTV")
    FIELDS = {
        "name": rid("nameET"),
        "card_number": rid("cardNumberET"),
        "expiration": rid("expirationDateET"),
        "cvv": rid("securityCodeET"),
    }
    REVIEW = rid("paymentBtn")

    def is_displayed(self):
        return self.is_present(self.HEADING)

    def fill(self, **values):
        self.find(self.FIELDS["name"])
        for key, value in values.items():
            self.type(self.FIELDS[key], value)
        self.hide_keyboard()
        return self

    def submit(self):
        self.tap(self.REVIEW)


class ReviewPage(BasePage):
    ITEM_PRICE = rid("priceTV")
    TOTAL = rid("totalAmountTV")

    def wait_loaded(self):
        self.find(self.TOTAL)
        return self

    def item_price(self):
        return price_value(self.text_of(self.ITEM_PRICE))

    def total(self):
        return price_value(self.text_of(self.TOTAL))

    def delivery_fee(self):
        return price_value(self.scroll_to("amountTV").text)

    def shown_card_number(self):
        return self.scroll_to("cardNumberTV").text

    def place_order(self):
        self.scroll_to("paymentBtn").click()


class CompletePage(BasePage):
    HEADING = rid("completeTV")
    CONTINUE = rid("shoopingBt")  # the app's own id is misspelled

    def heading(self):
        return self.text_of(self.HEADING)

    def continue_shopping(self):
        from pages.catalog_page import CatalogPage

        self.tap(self.CONTINUE)
        return CatalogPage(self.driver).wait_loaded()
