from pages.base_page import BasePage, price_value, rid


class CatalogPage(BasePage):
    IMAGES = rid("productIV")
    TITLES = rid("titleTV")
    PRICES = rid("priceTV")
    SORT = rid("sortIV")
    SORT_OPTIONS = {
        "name_asc": rid("nameAscCL"),
        "name_desc": rid("nameDesCL"),
        "price_asc": rid("priceAscCL"),
        "price_desc": rid("priceDesCL"),
    }

    def wait_loaded(self):
        self.find(self.TITLES)
        return self

    def title(self):
        return self.text_of(self.SCREEN_TITLE)

    def visible_products(self):
        """(name, price) for each product card whose title and price are on screen."""
        self.wait_loaded()
        names = [e.text for e in self.find_all(self.TITLES)]
        prices = [price_value(e.text) for e in self.find_all(self.PRICES)]
        return list(zip(names, prices))

    def sort_by(self, option):
        self.tap(self.SORT)
        self.tap(self.SORT_OPTIONS[option])
        return self.wait_loaded()

    def open_product(self, name):
        from pages.product_page import ProductPage

        self.wait_loaded()
        # Only the card image opens the product; the title text is not tappable.
        # Cards render image/title pairs in order, so the title's index is the image's.
        names = [e.text for e in self.find_all(self.TITLES)]
        self.find_all(self.IMAGES)[names.index(name)].click()
        return ProductPage(self.driver).wait_loaded()
