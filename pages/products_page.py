from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_list = (By.CLASS_NAME, "inventory_list")
        self.add_to_cart_buttons = (By.CLASS_NAME, "btn_inventory")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    def wait_for_products(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.product_list)
        )

    def add_product_to_cart(self, index):
        buttons = self.driver.find_elements(*self.add_to_cart_buttons)
        buttons[index].click()

    def get_cart_count(self):
        return int(self.driver.find_element(*self.cart_badge).text)

    def click_cart(self):
        self.driver.find_element(*self.cart_icon).click()
        
    def is_products_page_visible(self):
        try:
            self.wait_for_products()
            return True
        except:
            return False 